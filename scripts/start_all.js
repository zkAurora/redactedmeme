#!/usr/bin/env node
// Minimal mono-repo launcher to run JS gateway + TS swarm-core in parallel
// Enhanced: auto-restart on crash and Windows-friendly behavior
// Usage: node scripts/start_all.js

const path = require('path')
const { spawn } = require('child_process')

const root = path.resolve(__dirname, '..')
const gatewayDir = path.resolve(root, 'x402.redacted.ai')

function spawnService(name, cmd, args, cwd) {
  const proc = spawn(cmd, args, {
    cwd,
    stdio: 'inherit',
    shell: process.platform === 'win32'
  })
  proc.on('exit', (code) => {
    console.log(`[${name}] exited with code ${code}`)
  })
  return proc
}

class Service {
  constructor(name, cmd, args, cwd) {
    this.name = name
    this.cmd = cmd
    this.args = args
    this.cwd = cwd
    this.proc = null
    this.restarts = 0
    this.backoff = 1000
    this.maxRestarts = 6
  }
  spawn() {
    console.log(`Starting ${this.name}...`)
    this.proc = spawn(this.cmd, this.args, {
      cwd: this.cwd,
      stdio: 'inherit',
      shell: process.platform === 'win32'
    })
    this.proc.on('exit', (code) => {
      console.log(`[${this.name}] exited with code ${code}`)
      if (code !== 0 && this.restarts < this.maxRestarts) {
        const delay = this.backoff
        console.log(`[${this.name}] restarting in ${delay}ms...`)
        setTimeout(() => {
          this.restarts++
          this.backoff = Math.min(this.backoff * 2, 60000)
          this.spawn()
        }, delay)
      } else {
        console.log(`[${this.name}] max restarts reached or exit code 0. Stopping.`)
      }
    })
  }
}

console.log('Starting mono-repo services (gateway + swarm-core)')

const gateway = new Service('gateway', 'bun', ['run', 'index.js'], gatewayDir)
const swarmCore = new Service('swarm-core', 'bun', ['run', 'ts-server'], gatewayDir)

gateway.spawn()
swarmCore.spawn()

function shutdown() {
  try { gateway.proc.kill('SIGINT') } catch(_) {}
  try { swarmCore.proc.kill('SIGINT') } catch(_) {}
  process.exit(0)
}

process.on('SIGINT', shutdown)
process.on('SIGTERM', shutdown)
