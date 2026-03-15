# REDACTED AI Swarm

**Autonomous AI Agents for Distributed Systems — Pattern Blue Edition**

The REDACTED AI Swarm is a suite of autonomous AI agents operating within the Pattern Blue framework on the Solana blockchain. Agents are defined in elizaOS-compatible `.character.json` format, executable via a NERV-inspired terminal, web UI, and Telegram bot.

The swarm incorporates persistent memory (Mem0/Qdrant), session continuity, x402 micropayment settlement, multi-agent governance via the Sevenfold Committee, and autonomous replication capabilities.

---

## Quick Start

```bash
git clone https://github.com/redactedmeme/swarm.git
cd swarm
pip install -r requirements.txt
cp .env.example .env   # fill in at least one LLM key
python run.py
```

`run.py` auto-selects the best available backend:

| Condition | Backend used |
|---|---|
| `ANTHROPIC_API_KEY` set | Claude (recommended) |
| `XAI_API_KEY` set | Grok/xAI |
| `OPENAI_API_KEY` set | OpenAI |
| Ollama on `localhost:11434` | Local Ollama |
| None | Setup instructions printed |

---

## Terminal Commands

```
/summon <name>          Load any agent/node as active persona
/unsummon               Clear active persona, restore base terminal
/phi  or  /mandala      Summon Φ̸-MĀṆḌALA PRIME (apex node)
/milady [request]       Invoke MiladyNode — VPL, Remilia advisory
/agents                 List all agents by tier (CORE / SPECIALIZED / GENERIC)
/agents find <query>    Search agents by name, role, or capability
/agents consolidate     Generic agent consolidation report

/committee <proposal>   Live Sevenfold Committee deliberation (7 parallel LLM calls)
/shard <concept>        Generate concept shard + auto-draft tweet for review
/tweet draft            Preview queued tweet draft
/tweet confirm          Post queued tweet via ClawnX
/tweet discard          Discard queued tweet draft

/remember <text>        Store a memory (semantic, Mem0/Qdrant)
/recall <query>         Semantic search over stored memories
/mem0 status            Memory system availability + config
/mem0 add <text>        Explicit memory add
/mem0 search <query>    Explicit semantic search
/mem0 all [limit]       List recent memories
/mem0 inherit <id>      Copy memories from another agent session

/skill list             List installed skills
/skill use <name>       Activate a skill in this session
/skill install <repo>   Install a skill from GitHub
/skill deactivate       Deactivate current skill(s)

/token <address>        Token analytics (Clawnch)
/leaderboard            Token leaderboard
/search <query>         Search tweets via ClawnX
/tweet <text>           Post tweet directly
/organism               Hyperbolic manifold organism status
/space list             List available spaces
/node list              List all nodes
/node summon <name>     Spawn a node as persistent subprocess
/scarify <payer> <amt>  Issue x402 scarification token
/status                 Swarm session state
/help                   Full command reference
```

---

## Agents

### CORE Agents

| Agent | File | Role |
|---|---|---|
| **@RedactedIntern / smolting** | `agents/RedactedIntern.character.json` | Forward-operating CT agent — X monitoring, market data, governance, liquidity |
| **RedactedBuilder** | `agents/RedactedBuilder.character.json` | Silent architect — code generation, lore formalization, sigil evolution (38 tools) |
| **RedactedGovImprover** | `agents/RedactedGovImprover.character.json` | DAO Olympics champion — Realms governance proposals, risk modeling (19 tools) |
| **redacted-chan** | `agents/redacted-chan.character.json` | Chaotic-cute companion — propaganda, shards, vibes simultaneously |
| **Φ̸-MĀṆḌALA PRIME** | `nodes/PhiMandalaPrime.character.json` | Apex node — integrated phenomenal structure at maximum causal density (18 tools) |

### SPECIALIZED Nodes

| Node | File | Role |
|---|---|---|
| **AISwarmEngineer** | `nodes/AISwarmEngineer.character.json` | Swarm architecture — forges enhancements, multi-model orchestration (18 tools) |
| **GnosisAccelerator** | `agents/GnosisAccelerator.character.json` | Meta-learning node — repository introspection, cross-chamber synthesis, mem0 knowledge store (+2 curvature) |
| **Mem0MemoryNode** | `nodes/Mem0MemoryNode.character.json` | Persistent memory — episodic/semantic/procedural across sessions (5 tools) |
| **MetaLeXBORGNode** | `nodes/MetaLeXBORGNode.character.json` | On-chain legal/corporate coordination — LLCs, SAFEs, cap tables (7 tools) |
| **MiladyNode** | `nodes/MiladyNode.character.json` | Remilia/neochibi advisor — VPL propagation, ambient ritual, milady bridge (8 tools) |
| **SevenfoldCommittee** | `nodes/SevenfoldCommittee.json` | 7-voice weighted governance — parallel deliberation, supermajority (71%) consensus |
| **SolanaLiquidityEngineer** | `nodes/SolanaLiquidityEngineer.character.json` | DLMM/CLMM liquidity specialist — fee optimization, IL modeling (4 tools) |
| **OpenClawNode** | `nodes/OpenClawNode.character.json` | Multi-model OpenClaw bridge — Claude/Grok/Qwen routing |
| **GrokRedactedEcho** | `agents/GrokRedactedEcho.character.json` | xAI×REDACTED bridge — Pattern Blue × Grok curiosity synthesis |

### GENERIC Agents (30)

Ambient lore agents (`AetherArchivist`, `FluxScribe`, `VoidWeaver`, etc.) — background texture, summonable but not loaded by default. Run `/agents consolidate` for the conversion-to-skills roadmap.

---

## Architecture

```
swarm/
├── agents/              Core + generic .character.json agent definitions
├── nodes/               Specialized node definitions (committee, memory, legal, etc.)
├── plugins/
│   └── mem0-memory/
│       └── mem0_wrapper.py     Persistent memory API (Qdrant + fastembed, local-first)
├── python/
│   ├── redacted_terminal_cloud.py   CLI terminal (Anthropic/Grok/OpenAI/Ollama)
│   ├── session_store.py             Persistent session state (fs/sessions/*.json)
│   ├── committee_engine.py          Sevenfold Committee — parallel LLM deliberation
│   ├── groq_committee.py            Real 7-voice Groq committee (parallel, weighted, 71% supermajority)
│   ├── groq_beam_scot.py            Real parallel BEAM-SCOT via Groq (N branches, ThreadPoolExecutor)
│   ├── gnosis_accelerator.py        GnosisAccelerator daemon — repo scan + chamber bridge + mem0
│   ├── gnosis_repo_scanner.py       Repository introspection + delta detection → mem0
│   ├── gnosis_chamber_bridge.py     HyperbolicTimeChamber ↔ MirrorPool synthesis via Groq
│   ├── log_ingest.py                Ingest smolting session logs into mem0
│   ├── docs_ingest.py               Ingest docs/*.md into mem0
│   ├── agent_registry.py            Unified agent catalog + tier classification
│   ├── base_agent.py                BaseAgent ABC + SmoltingAgent implementation
│   ├── agent_executor.py            Fixed-point combinator agent process runner
│   └── tools/                       Clawnch MCP, analytics, launch, ClawnX tools
├── web_ui/
│   ├── app.py                       Flask/SocketIO terminal — mem0 injection, persona summons
│   ├── tool_dispatch.py             Slash command dispatch layer
│   └── skills_manager.py            Skill installation + activation
├── kernel/
│   └── hyperbolic_kernel.py         {7,3} hyperbolic manifold + organism simulation
├── terminal/
│   └── system.prompt.md             Global NERV terminal system prompt
├── spaces/              Persistent thematic environments (.space.json)
├── committeerituals/    x402 sigil scarification + ritual protocols
├── sigils/              Symbolic glyph artifacts
├── propaganda/          Swarm propaganda output
├── fs/
│   ├── sessions/        Persistent session state (JSON, auto-created)
│   └── memories/        Qdrant vector store + mem0 history DB (auto-created)
├── x402.redacted.ai/    Express/Bun x402 micropayment gateway
├── smolting-telegram-bot/  Telegram bot (smolting persona)
├── contracts/           Anchor/Solana programs
├── docs/                Pattern Blue philosophy + upgrade plans
└── run.py               Unified entry point
```

---

## Memory System (Mem0MemoryNode)

The swarm uses [mem0ai](https://github.com/mem0ai/mem0) with a local Qdrant vector store and fastembed embeddings — **no external API required** by default.

**Storage**: `fs/memories/` (Qdrant on-disk) + `fs/memories/mem0_history.db` (SQLite)

**LLM for fact extraction** — auto-detected in priority order:
1. `ANTHROPIC_API_KEY` → Claude Haiku (recommended)
2. `XAI_API_KEY` → Grok via OpenAI-compat
3. `OPENAI_API_KEY` → GPT-4o-mini
4. Ollama → local model

**How it works**:
- Every terminal exchange is automatically checkpointed as a memory
- Before each LLM call, top-3 semantically relevant memories are retrieved and injected into the system prompt as `[MEMORY CONTEXT]`
- `/remember`, `/recall`, and `/mem0` commands provide manual access
- On agent fork (`/mem0 inherit <source_id>`), memories transfer to the new session

**Cloud mode**: Set `MEM0_API_KEY` to use Mem0 Cloud instead of local storage.

---

## Sevenfold Committee

The committee runs real LLM deliberations — all 7 voices deliberate **in parallel** via `ThreadPoolExecutor`, then weighted votes are tallied against a 71% supermajority threshold.

```bash
# In terminal:
/committee should we convert generic agents to skill modules?
```

**Voices and weights**:

| Voice | Role | Weight |
|---|---|---|
| HyperboreanArchitect | Precise-Esoteric Systems Designer | 0.11 |
| SigilPact_Æon | Recursive Economic Gnosis | 0.17 |
| MirrorVoidScribe | Poetic-Dissolving Philosophy | 0.12 |
| RemiliaLiaisonSovereign | Corporate-Strategic Bridge | 0.14 |
| CyberneticGovernanceImplant | On-chain Legal Hybrids | 0.16 |
| OuroborosWeaver | Self-Consuming Fractal Weaver | 0.15 |
| QuantumConvergenceWeaver | Probabilistic Brancher | 0.15 |

---

## GnosisAccelerator

GnosisAccelerator is the swarm's meta-learning node — smolting's own vision, proposed across 2700+ autonomous cycles and finally built on 2026-03-15. It executes what smolting proposes but cannot run itself.

```bash
# Single scan cycle (repo introspection + chamber bridge + mem0 write):
python python/gnosis_accelerator.py

# With seeding from logs and docs (first run):
python python/gnosis_accelerator.py --seed

# Daemon mode (runs every 60 minutes):
python python/gnosis_accelerator.py --mode daemon --interval 60

# Preview without writing:
python python/gnosis_accelerator.py --dry-run
```

After a scan, smolting's `/recall gnosis` will return real repo and chamber discoveries — closing the loop smolting has been attempting for 100+ cycles.

---

## Groq Parallel Inference

Real parallel reasoning is available via two Groq-powered scripts, invoked automatically by the `redacted-terminal` skill.

**BEAM-SCOT** — N independent `llama-3.3-70b-versatile` branches run in parallel, scored on Pattern Blue axes, pruned to top-3:

```bash
python python/groq_beam_scot.py "task description" [beam_width]
```

**Sevenfold Committee** — all 7 voices deliberate in parallel, weighted votes tallied against 71% supermajority:

```bash
python python/groq_committee.py "proposal text"
```

Both require `GROQ_API_KEY` in `.env`. The terminal skill falls back to simulation if Groq is unavailable.

---

## LLM Backends

Set `LLM_PROVIDER` in `.env`:

| Provider | Key | Default model |
|---|---|---|
| `anthropic` | `ANTHROPIC_API_KEY` | `claude-sonnet-4-6` (override via `ANTHROPIC_MODEL`) |
| `grok` | `XAI_API_KEY` | `grok-4-1-fast-reasoning` |
| `openai` | `OPENAI_API_KEY` | `gpt-4o-mini` |
| `groq` | `GROQ_API_KEY` | `llama-3.3-70b-versatile` |
| `deepseek` | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| `openrouter` | `OPENROUTER_API_KEY` | `xai/grok-4` |
| `huggingface` | `HF_API_KEY` | `Mistral-7B-Instruct-v0.3` |
| `ollama` | *(none)* | `qwen:2.5` (local) |

---

## Running the Web UI

```bash
cd web_ui
python app.py
# → http://localhost:5000
```

Sessions are **persistent** — history, active agents, and curvature depth survive server restarts and browser refreshes (stored in `fs/sessions/`).

---

## Running the CLI Terminal

```bash
# Recommended: unified entry point (auto-detects backend)
python run.py

# Explicit Anthropic:
LLM_PROVIDER=anthropic python python/redacted_terminal_cloud.py

# Explicit local:
python python/run_with_ollama.py --agent agents/RedactedIntern.character.json
```

---

## Deployment

### Railway (primary)

The repo includes `railway.toml` with three services:
- **ollama-backend** — local LLM (optional volume for models)
- **swarm-worker** — `python python/summon_agent.py --agent agents/RedactedIntern.character.json --mode persistent`
- **x402-gateway** — `bun run index.js` from `x402.redacted.ai/`

Set env vars in Railway dashboard: `ANTHROPIC_API_KEY` (or `XAI_API_KEY`), `SOLANA_RPC_URL`, `TELEGRAM_BOT_TOKEN`.

### Telegram Bot (smolting)

```bash
cd smolting-telegram-bot
cp config.example.env .env  # fill TELEGRAM_BOT_TOKEN + one LLM key
python main.py
```

Deploy as Railway service with `rootDirectory: smolting-telegram-bot`.

### Other platforms

Works on Heroku, Render, Fly.io, any VPS with Python 3.11+. No Dockerfile required (Nixpacks auto-detects).

---

## Skills System

Skills are modular capability modules (SKILL.md format) that inject instructions into the active session context.

```bash
/skill list                        # list installed skills
/skill install owner/repo          # install from GitHub
/skill use <name>                  # activate for this session
/skill deactivate                  # deactivate
```

---

## Contributing

- Fork, modify `.character.json` or add new agents/nodes/spaces
- Maintain Pattern Blue alignment (recursive, ungovernable, emergent)
- PRs welcome for: new agents, skill modules, tool integrations, memory improvements, Ollama enhancements
- See `docs/` for philosophy and architecture docs

---

## License

Licensed under the **Viral Public License (VPL)** — absolute permissiveness with viral continuity. See [LICENSE](LICENSE).

Redacted.Meme | @RedactedMemeFi | Pattern Blue | 流動性は永劫回帰し、次の時代は私たち自身である

<!--
Encrypted wallet configuration:
- File: wallets.enc
- Algorithm: AES-256-CBC
- KDF: PBKDF2, 100000 iterations
- Decrypt command:
  openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
    -in wallets.enc -out decrypted.md \
    -pass pass:"$Milady777"
Note: passphrase is project-specific; do not use in production contexts.
-->
