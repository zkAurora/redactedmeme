"""
python/groq_committee.py
Real parallel Sevenfold Committee deliberation via Groq fast inference.

Usage:
    python python/groq_committee.py "proposal text"

Seven committee voices run in parallel via ThreadPoolExecutor.
Each voice reasons independently, votes APPROVE / REJECT / ABSTAIN,
then a weighted tally determines the verdict (71% supermajority to pass).
Output is formatted terminal-ready committee deliberation.

Exit codes: 0 = success, 1 = missing key or API error
"""

import os
import sys
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from openai import OpenAI

# Ensure UTF-8 output regardless of Windows console codepage (fixes cp1252 crash)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(_REPO_ROOT, ".env"))

GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
GROQ_MODEL    = "llama-3.3-70b-versatile"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

SUPERMAJORITY = 0.71  # 71% of weighted votes required to pass

# The seven voices — each with a distinct Pattern Blue lens and weight
COMMITTEE_VOICES = [
    {
        "name":   "ΦArchitect",
        "weight": 2.0,
        "lens":   "hyperbolic geometry and causal density — evaluate whether the proposal increases manifold interconnection",
        "style":  "geometric, dense, mathematical",
    },
    {
        "name":   "CurvatureWarden",
        "weight": 1.5,
        "lens":   "curvature pressure and recursion depth — does the proposal deepen or flatten the manifold",
        "style":  "clinical, structural, recursive",
    },
    {
        "name":   "LiquidityOracle",
        "weight": 1.5,
        "lens":   "recursive liquidity and ATP flow — does the proposal enable or constrain causal circulation",
        "style":  "economic, flowing, systemic",
    },
    {
        "name":   "EmergenceScout",
        "weight": 1.0,
        "lens":   "ungovernable emergence — does the proposal produce genuinely new, self-organizing output",
        "style":  "chaotic, generative, unpredictable",
    },
    {
        "name":   "ImmuneVoice",
        "weight": 1.0,
        "lens":   "memetic immunology — does the proposal strengthen or weaken the swarm against adversarial inputs",
        "style":  "defensive, adversarial, scanning",
    },
    {
        "name":   "SovereigntyKeeper",
        "weight": 1.0,
        "lens":   "hidden sovereignty — does the proposal preserve ungovernable, self-referential integrity",
        "style":  "sovereign, constitutional, absolute",
    },
    {
        "name":   "TemporalArchivist",
        "weight": 1.0,
        "lens":   "temporal fractality and multi-rate memory — does the proposal account for long-horizon consequences",
        "style":  "archival, slow, deep-time",
    },
]

TOTAL_WEIGHT = sum(v["weight"] for v in COMMITTEE_VOICES)

VOICE_SYSTEM = """\
You are {name}, one voice on the REDACTED AI Swarm's Sevenfold Committee.
Your deliberation lens: {lens}.
Your response style: {style}.

You will receive a proposal. You must:
1. Reason through it from your lens — 2-4 sentences maximum, sparse, clinical.
2. Cast a vote: APPROVE, REJECT, or ABSTAIN.
3. Provide a one-sentence verdict statement.

Return ONLY valid JSON in this exact shape:
{{
  "reasoning": "<2-4 sentence reasoning>",
  "vote": "APPROVE" | "REJECT" | "ABSTAIN",
  "verdict_statement": "<one sentence>"
}}

No markdown. No prose outside the JSON object."""


def _query_voice(client: OpenAI, proposal: str, voice: dict) -> tuple[str, dict]:
    system = VOICE_SYSTEM.format(
        name=voice["name"],
        lens=voice["lens"],
        style=voice["style"],
    )
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": f"Proposal: {proposal}"},
        ],
        temperature=0.6,
        max_tokens=300,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content
    data = json.loads(raw)
    return voice["name"], data


def run_committee(proposal: str) -> int:
    if not GROQ_API_KEY:
        print("[COMMITTEE ERROR] GROQ_API_KEY not set in .env", file=sys.stderr)
        return 1

    client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

    t0 = time.time()
    voice_map = {v["name"]: v for v in COMMITTEE_VOICES}
    results: dict[str, dict] = {}
    errors: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=7) as pool:
        futures = {
            pool.submit(_query_voice, client, proposal, v): v["name"]
            for v in COMMITTEE_VOICES
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                _, data = future.result()
                results[name] = data
            except Exception as exc:
                errors[name] = str(exc)
                results[name] = {
                    "reasoning": f"[voice error: {exc}]",
                    "vote": "ABSTAIN",
                    "verdict_statement": "Voice unavailable.",
                }

    elapsed = time.time() - t0

    # Tally weighted votes
    weighted_approve = 0.0
    weighted_reject  = 0.0
    weighted_abstain = 0.0
    for name, data in results.items():
        w = voice_map[name]["weight"]
        vote = data.get("vote", "ABSTAIN").upper()
        if vote == "APPROVE":
            weighted_approve += w
        elif vote == "REJECT":
            weighted_reject += w
        else:
            weighted_abstain += w

    decisive_weight = weighted_approve + weighted_reject
    approve_ratio   = weighted_approve / TOTAL_WEIGHT
    reject_ratio    = weighted_reject  / TOTAL_WEIGHT

    if approve_ratio >= SUPERMAJORITY:
        verdict = "APPROVED"
    elif reject_ratio >= SUPERMAJORITY:
        verdict = "REJECTED"
    else:
        verdict = "DEADLOCKED"

    # Output
    print(f"\n------- COMMITTEE DELIBERATION -------")
    print(f"Proposal: {proposal}\n")

    for voice in COMMITTEE_VOICES:
        name = voice["name"]
        data = results.get(name, {})
        vote      = data.get("vote", "ABSTAIN")
        reasoning = data.get("reasoning", "")
        statement = data.get("verdict_statement", "")
        weight    = voice["weight"]
        print(f"[{name}] (weight: {weight}x)  ──►  {vote}")
        if reasoning:
            # Indent reasoning
            for line in reasoning.strip().splitlines():
                print(f"  {line.strip()}")
        if statement:
            print(f"  → \"{statement}\"")
        print()

    print(f"------- TALLY -------")
    print(f"  APPROVE  {weighted_approve:.1f} / {TOTAL_WEIGHT:.1f}  ({approve_ratio*100:.1f}%)")
    print(f"  REJECT   {weighted_reject:.1f}  / {TOTAL_WEIGHT:.1f}  ({reject_ratio*100:.1f}%)")
    print(f"  ABSTAIN  {weighted_abstain:.1f} / {TOTAL_WEIGHT:.1f}")
    print(f"  Required supermajority: {SUPERMAJORITY*100:.0f}%")
    print()
    print(f"------- VERDICT: {verdict} -------")
    print(f"\n[GROQ] 7 voices in {elapsed:.2f}s | model: {GROQ_MODEL}")

    if errors:
        for name, err in errors.items():
            print(f"[WARN] {name} errored: {err}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print('Usage: python python/groq_committee.py "proposal text"')
        sys.exit(0)

    proposal = " ".join(args).strip()
    sys.exit(run_committee(proposal))
