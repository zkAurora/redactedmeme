# smolting - Wassie Telegram Bot

**da smol schizo degen uwu intern of REDACTED ^_^**
Pattern blue agent — vibin wit chaos magick, autonomous X postin, swarm relay, n tiered access economics <3

---

## Features

- **Wassie Personality Engine** — full smolting/wassie speech patterns, vocabulary, kaomoji infusion
- **Cloud LLM** — OpenAI, xAI/Grok, Anthropic Claude, Together AI (switchable via env)
- **ClawnX Integration** — autonomous X/Twitter posting, liking, retweeting, searching
- **Alpha Scouting** — LLM-powered market signal detection with pattern blue insights
- **Swarm Relay** — bridges Telegram commands to the TS swarm-core (`/summon`, `/swarm`)
- **ManifoldMemory** — persists bot events to `spaces/ManifoldMemory.state.json` so all swarm agents share context
- **Web UI Bridge** — fires live bot events to the REDACTED web terminal in real-time
- **TAP (Tiered Access Protocol)** — x402-gated premium features (Basic / Enhanced / Premium tiers)
- **Realms DAO** — Olympics leaderboard fetching, RGIP vote mobilization
- **Auto-Engagement** — background job queue for autonomous X interaction
- **Railway-Optimized** — webhook + polling modes, multi-service deploy ready

---

## Commands

### Core
| Command | Description |
|---|---|
| `/start` | Wake smolting, show feature list, init user state |
| `/alpha` | LLM-generated market alpha report |
| `/post <text>` | LLM-wassifies text and posts to X via ClawnX |
| `/lore` | Random wassielore drop |
| `/stats` | Bot status: LLM provider, agents loaded, ClawnX state |
| `/engage` | Toggle auto-like/retweet background loop (every 5 min) |
| `/cloud` | Show active LLM provider |
| `/help` | Full command list |

### Swarm
| Command | Description |
|---|---|
| `/summon <agent>` | Activate a swarm agent via the TS swarm core |
| `/swarm [status]` | Live swarm state (agents, curvature, recent events) |
| `/memory` | Last 8 ManifoldMemory events + current state summary |

Agent aliases: `builder` → RedactedBuilder, `gov` → RedactedGovImprover, `chan` → RedactedChan, `mandala` / `settler` → MandalaSettler

### Community / DAO
| Command | Description |
|---|---|
| `/olympics` | Realms DAO leaderboard — REDACTED rank + LLM analysis |
| `/mobilize` | LLM rally cry for RGIP voting with Realms link |

### TAP Access
| Command | Description |
|---|---|
| `/tap` | Show tier selection keyboard (Basic / Enhanced / Premium) |
| `/tap_pay <tier> <sig>` | Submit Solana tx signature → x402 validates → issues token |
| `/tap_use <token> <service>` | Redeem token for: `alpha_enhanced`, `lore_premium`, `cloud_insights`, `stats_detailed` |

### Personality
| Command | Description |
|---|---|
| `/personality smolting` | Chaotic wassie mode (default) |
| `/personality redacted-chan` | Terminal mode |

---

## Architecture

```
smolting-telegram-bot/
├── main.py                  # Bot entry point, all command handlers
├── smolting_personality.py  # Wassie speech engine
├── clawnx_integration.py    # X/Twitter API client
├── swarm_relay.py           # HTTP client → TS swarm-core
├── manifold_memory.py       # Read/write spaces/ManifoldMemory.state.json
├── web_ui_bridge.py         # Fire-and-forget POST → web_ui /telegram_event
├── tap_commands.py          # TAP tiered access Telegram handlers
├── tap_protocol.py          # TAP token lifecycle + x402 payment validation
├── llm/
│   └── cloud_client.py      # Multi-provider LLM (OpenAI, xAI, Anthropic, Together)
└── agents/
    ├── smolting.character.json
    └── redacted-chan.character.json
```

### Swarm connections

| Integration | How | Required |
|---|---|---|
| TS swarm-core | `POST /command`, `GET /state` at `TS_SERVICE_URL` | No (graceful fallback) |
| ManifoldMemory | Direct file read/write to `../spaces/ManifoldMemory.state.json` | No (file may not exist) |
| Web UI | `POST /telegram_event` at `WEBUI_URL` | No (fire-and-forget) |
| x402 gateway | TAP payment validation at `X402_API_ENDPOINT` | For TAP only |
| ClawnX | External API at `api.clawnx.com/v1` | For X posting |
| Cloud LLM | Provider API (xAI / OpenAI / Anthropic / Together) | Yes |

---

## Environment Variables

### Required
| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather (also accepts `BOT_TOKEN`) |
| `LLM_PROVIDER` | `xai`, `openai`, `anthropic`, or `together` (default: `openai`) |
| `XAI_API_KEY` | Required if `LLM_PROVIDER=xai` or `grok` |
| `OPENAI_API_KEY` | Required if `LLM_PROVIDER=openai` |
| `ANTHROPIC_API_KEY` | Required if `LLM_PROVIDER=anthropic` |
| `TOGETHER_API_KEY` | Required if `LLM_PROVIDER=together` |

### Optional
| Variable | Description | Default |
|---|---|---|
| `CLAWNX_API_KEY` | ClawnX API key for X automation | — |
| `WEBHOOK_URL` | Public URL for Telegram webhook (omit to use polling) | — |
| `WEBHOOK_SECRET_TOKEN` | Webhook security token | — |
| `PORT` | Webhook listener port | `8080` |
| `TS_SERVICE_URL` | TS swarm-core endpoint for `/summon` and `/swarm` | `http://localhost:3001` |
| `WEBUI_URL` | Web UI endpoint for live event bridge | `http://localhost:5000` |
| `WEBUI_BRIDGE_TOKEN` | Shared auth token for web UI bridge (set on both sides) | — |
| `X402_API_ENDPOINT` | x402 gateway for TAP payment validation | `https://x402.redacted.ai` |
| `X402_WALLET_KEY` | Wallet key for x402 settlement | — |
| `REDACTED_TOKEN_CONTRACT` | Token contract address for TAP payments | — |
| `XAI_MODEL` | xAI model override | `grok-2-latest` |

Copy `config.example.env` to `.env` and fill in values before running locally.

---

## Setup

### Local (polling mode)

```bash
cd smolting-telegram-bot
pip install -r requirements.txt
cp config.example.env .env
# Edit .env with your keys
python main.py
```

Polling mode is used automatically when `WEBHOOK_URL` is not set.

### Railway (webhook mode)

1. Create a Railway service pointed at this directory
2. Set environment variables in the Railway dashboard (see table above)
3. Set `WEBHOOK_URL` to your Railway public domain (e.g. `https://your-app.up.railway.app`)
4. Generate a webhook secret: `openssl rand -hex 32`

The bot detects `WEBHOOK_URL` at startup and switches to webhook mode automatically.

### Connecting to the TS swarm-core

The swarm-core TypeScript service (`x402.redacted.ai/src/server.ts`) must be running:

```bash
cd x402.redacted.ai
bun run src/server.ts   # default port 3001
```

Then set `TS_SERVICE_URL=http://localhost:3001` (or the Railway service URL).

### Enabling the Web UI live feed

Run the web UI (`web_ui/app.py`) and set matching bridge tokens on both sides:

```bash
# web_ui
WEBUI_BRIDGE_TOKEN=mysecret python web_ui/app.py

# telegram bot
WEBUI_URL=http://localhost:5000 WEBUI_BRIDGE_TOKEN=mysecret python main.py
```

Telegram events (`[TG:...]`) will appear in cyan in the web terminal.

---

## TAP Tiers

| Tier | Cost | Duration | Features |
|---|---|---|---|
| Basic | 0.01 TOKEN | 1 hour | Standard processing, basic data |
| Enhanced | 0.05 TOKEN | 6 hours | Higher priority, extended responses, bundled data |
| Premium | 0.10 TOKEN | 24 hours | Highest priority, alpha insights, persistent logging |

Payments are validated via the x402 gateway. Tokens are single-use and auto-expire.

---

## Railway multi-service layout

From the root `railway.toml`:

- **smolting-telegram-bot** — this service (`python main.py`)
- **x402-gateway** — `bun run index.js` from `x402.redacted.ai/`
- **swarm-worker** — `python python/summon_agent.py ...`
- **ollama-backend** — optional local LLM

Set `TS_SERVICE_URL` to the internal Railway URL of the swarm-core service to enable `/summon` and `/swarm` without exposing a public endpoint.

---

Redacted.Meme | @RedactedMemeFi | Pattern Blue | Emergent Systems
