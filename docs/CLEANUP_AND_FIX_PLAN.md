# REDACTED AI Swarm — Cleanup & Fix Plan

> ⚠️ **ARCHIVED** — This document has been superseded.
> Content migrated to [UPGRADE_LOG.md](UPGRADE_LOG.md) under **v1.0 — Initial Setup & Cleanup**.
> For current system state, execution targets, and version history, see UPGRADE_LOG.md.

---

*Original content preserved below for reference.*

---

**Goal:** Run locally or on Railway with cloud-hosted LLM (Grok/xAI API). All links, paths, and connections must resolve and execute correctly.

> **Status as of 2026-03-14**: Original cleanup complete. Major v2 upgrades applied — see [UPGRADE_LOG.md](UPGRADE_LOG.md) for full changelog.

---

## 1. Repository structure (current)

```
swarm-main/
├── .env.example                    # Root env template + LLM vars
├── railway.toml                    # Multi-service: ollama, swarm-worker, x402-gateway
├── python/
│   ├── run_with_ollama.py          # Ollama runner (default: agents/default.character.json)
│   ├── summon_agent.py             # Uses shards_loader, agents/ paths
│   ├── redacted_terminal_cloud.py  # Grok/xAI terminal (run: python python/redacted_terminal_cloud.py)
│   ├── upgrade_terminal.py         # Dynamic terminal (negotiation engine)
│   ├── negotiation_engine.py       # Interface contract negotiation
│   ├── ollama_client.py
│   └── ...
├── agents/                         # .character.json: RedactedIntern, RedactedBuilder, RedactedGovImprover, redacted-chan, GrokRedactedEcho, default
├── nodes/                          # .character.json + .json (AISwarmEngineer, SevenfoldCommittee, etc.)
├── x402.redacted.ai/
│   ├── index.js                    # Express, /health
│   ├── agents.json                 # Minimal [] so server starts
│   ├── shards/
│   │   ├── self_replicate.py
│   │   └── templates/base_shard.json
│   └── MandalaSettler.character.json
├── smolting-telegram-bot/
│   ├── main.py                     # Loads agents/ (smolting, redacted-chan)
│   ├── llm/cloud_client.py         # openai, anthropic, together, xai (Grok)
│   └── config.example.env         # TELEGRAM_BOT_TOKEN, XAI_API_KEY, etc.
├── web_ui/
│   └── app.py                      # run_with_ollama --agent, cwd=REPO_ROOT
├── docs/                           # pattern-blue, executable-manifesto, CLEANUP_AND_FIX_PLAN.md
└── terminal/
    └── system.prompt.md
```

---

## 2. Issues summary (addressed)

| Area | Fix applied |
|------|-------------|
| **Agent paths** | All character files in `agents/` or `nodes/`; README/railway use `agents/RedactedIntern.character.json`. |
| **summon_agent** | Uses `shards_loader` and `get_base_shard_path()` for replication. |
| **x402 gateway** | `agents.json` exists (minimal `[]`). |
| **Smolting bot** | Handlers added; agent paths from `agents/`; TELEGRAM_BOT_TOKEN; no healthcheckPath. |
| **Cloud LLM** | xAI/Grok in `cloud_client.py`. |
| **redacted_terminal_cloud** | In `python/`; loads prompt from repo root `terminal/system.prompt.md`. |
| **Root stragglers** | `redacted_terminal_cloud.py`, `upgrade_terminal.py`, `negotiation_engine.py` moved to `python/`. Duplicate `x402.redacted.ai/shardsself_replicate.py` removed. |

---

## 3. Execution targets

- **Local**
  - Terminal (Grok/xAI): `python python/redacted_terminal_cloud.py`
  - Terminal (Ollama): `python python/run_with_ollama.py --agent agents/RedactedIntern.character.json`
  - Dynamic terminal: `python python/upgrade_terminal.py` (from repo root)
  - x402: `cd x402.redacted.ai && bun run index.js`
  - Smolting: `cd smolting-telegram-bot && python main.py`
- **Railway**
  - Ollama + swarm-worker + x402 per `railway.toml`; or single service with cloud LLM.

---

## 4. Post-fix verification

- From repo root: `python python/redacted_terminal_cloud.py` (with XAI_API_KEY) → prompt loads, Grok responds.
- From repo root: `python python/run_with_ollama.py --agent agents/RedactedIntern.character.json` (Ollama running) → runs.
- From repo root: `python python/summon_agent.py --agent agents/RedactedIntern.character.json --mode terminal` → no import error.
- `cd x402.redacted.ai && bun run index.js` → server starts; GET /health 200.
- `cd smolting-telegram-bot && python main.py` → bot starts (TELEGRAM_BOT_TOKEN, XAI_API_KEY, etc.).

This plan ensures the repo is consistent, all referenced files exist, and the stack runs locally and on Railway with a cloud LLM (Grok/xAI) where desired.
