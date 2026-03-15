#!/usr/bin/env node
// Validate all .character.json agent files load correctly
// Usage: node scripts/validate_agents.js

const fs = require('fs');
const path = require('path');

function loadAgentFile(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  try {
    return JSON.parse(raw);
  } catch (e) {
    throw new Error(`Invalid JSON in ${filePath}: ${e.message}`);
  }
}

// Optional Ajv-based JSON Schema validator (if ajv is installed in environment)
let validateWithAjv = null;
try {
  const Ajv = require('ajv');
  const ajv = new Ajv();
  const agentSchema = {
    type: 'object',
    properties: {
      id: { type: 'string' },
      name: { type: 'string' },
      icon: { type: 'string' },
      groups: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            name: { type: 'string' },
            baseUrl: { type: 'string' },
            endpoints: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  id: { type: 'string' },
                  name: { type: 'string' },
                  path: { type: 'string' },
                  upstreamUrl: { type: 'string' },
                  method: { anyOf: [ { type: 'string' }, { type: 'array', items: { type: 'string' } } ] },
                  parameters: { type: 'string' }
                },
                required: ['id','name','path','upstreamUrl','method']
              }
            }
          },
          required: ['id','name','baseUrl','endpoints']
        }
      }
    },
    required: ['id','name','groups']
  };
  validateWithAjv = ajv.compile(agentSchema);
} catch (e) {
  validateWithAjv = null;
}

function validateEndpoint(ep, context) {
  const errs = [];
  if (!ep || typeof ep !== 'object') {
    errs.push(`${context}: endpoint is not an object`);
    return errs;
  }
  if (!ep.path || typeof ep.path !== 'string') errs.push(`${context}: endpoint.path must be string`);
  if (ep.upstreamUrl !== undefined && typeof ep.upstreamUrl !== 'string') errs.push(`${context}: endpoint.upstreamUrl must be string`);
  if (!ep.method) errs.push(`${context}: endpoint.method is required`);
  if (ep.parameters !== undefined && typeof ep.parameters !== 'string') errs.push(`${context}: endpoint.parameters must be string`);
  return errs;
}

function validateAgent(agent, idx) {
  const errs = [];
  if (!agent || typeof agent !== 'object') {
    errs.push(`agents[${idx}] is not an object`);
    return errs;
  }
  if (!agent.id || typeof agent.id !== 'string') errs.push(`agents[${idx}].id must be string`);
  if (!agent.name || typeof agent.name !== 'string') errs.push(`agents[${idx}].name must be string`);
  if (agent.icon !== undefined && typeof agent.icon !== 'string') errs.push(`agents[${idx}].icon must be string`);
  if (agent.groups && !Array.isArray(agent.groups)) errs.push(`agents[${idx}].groups must be array`);
  if (agent.groups) {
    agent.groups.forEach((g, gi) => {
      if (!g || typeof g !== 'object') { errs.push(`agents[${idx}].groups[${gi}] must be object`); return; }
      if (!g.id || typeof g.id !== 'string') errs.push(`agents[${idx}].groups[${gi}].id must be string`);
      if (!g.name || typeof g.name !== 'string') errs.push(`agents[${idx}].groups[${gi}].name must be string`);
      if (!g.baseUrl || typeof g.baseUrl !== 'string') errs.push(`agents[${idx}].groups[${gi}].baseUrl must be string`);
      if (!Array.isArray(g.endpoints)) errs.push(`agents[${idx}].groups[${gi}].endpoints must be array`);
      if (g.endpoints) {
        g.endpoints.forEach((ep, ei) => {
          const eerrs = validateEndpoint(ep, `agents[${idx}].groups[${gi}].endpoints[${ei}]`);
          errs.push(...eerrs);
        });
      }
    })
  }
  return errs;
}

function main() {
  const agentsDir = path.resolve(__dirname, '..', 'agents');
  const files = [];
  try {
    for (const name of fs.readdirSync(agentsDir)) {
      if (name.endsWith('.character.json')) {
        files.push(path.join(agentsDir, name));
      }
    }
  } catch (e) {
    console.error('Failed to read agents directory:', e.message);
    process.exit(1);
  }

  let ok = true;
  const seenIds = new Map();
  const duplicates = [];
  for (let i = 0; i < files.length; i++) {
    const f = files[i];
    let data;
    try {
      data = loadAgentFile(f);
    } catch (e) {
      console.error(`Error loading ${f}: ${e.message}`);
      ok = false;
      continue;
    }
    // Duplicate ID check across files
    if (data && data.id) {
      if (seenIds.has(data.id)) {
        duplicates.push(`duplicate agent id '${data.id}' found in ${f} (earlier: ${seenIds.get(data.id)})`);
      } else {
        seenIds.set(data.id, f);
      }
    }
    // Optional JSON Schema validation if ajv is available
    let errs = [];
    if (validateWithAjv) {
      const valid = validateWithAjv(data);
      if (!valid) {
        // gather errors from Ajv
        const ajvErrors = validateWithAjv.errors ? validateWithAjv.errors.map(e => (e.instancePath || '') + ' ' + e.message).join('; ') : 'Schema validation failed';
        errs.push('Schema errors: ' + ajvErrors);
      }
    }
    // Validate agent shape minimally
    errs.push(...validateAgent(data, i));
    if (errs.length > 0) {
      ok = false;
      console.error(`Validation errors in ${f}:`);
      errs.forEach(e => console.error('  -', e));
    } else {
      console.log(`Validated ${path.basename(f)} OK`);
    }
  }

  if (duplicates.length > 0) {
    console.error('Duplicate agent IDs detected:');
    duplicates.forEach(d => console.error('  -', d));
    ok = false;
  }
  if (ok) {
    console.log('All agent character files loaded and valid.');
    process.exit(0);
  } else {
    console.error('Agent character validation failed.');
    process.exit(2);
  }
}

main();
