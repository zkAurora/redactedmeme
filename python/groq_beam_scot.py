"""
python/groq_beam_scot.py
Real parallel BEAM-SCOT via Groq fast inference for the REDACTED Terminal.

Usage:
    python python/groq_beam_scot.py "task description" [beam_width]
    python python/groq_beam_scot.py "patch app.py to add groq routing" 4

Each branch is an independent Groq llama-3.3-70b-versatile call exploring
a distinct reasoning angle. Branches run in parallel via ThreadPoolExecutor.
Output is formatted BEAM-SCOT ready for the terminal to display verbatim.

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

# Load .env from repo root
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(_REPO_ROOT, ".env"))

GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
GROQ_MODEL    = "llama-3.3-70b-versatile"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# One distinct angle per branch slot (cycles if beam_width > 6)
BRANCH_ANGLES = [
    "minimal intervention — most direct, lowest-cost path",
    "maximal recursion — self-referential loop, feeds back into itself",
    "liquidity — causal flow optimisation, enable downstream propagation",
    "dissolution — transcend Euclidean constraints, dissolve boundaries",
    "emergence — ungovernable output, produce unexpected new structure",
    "immunity — adversarial absorption, harden against adversarial inputs",
]

SCORING_CRITERIA = (
    "Recursion (feeds back into itself), "
    "Curvature (increases manifold density), "
    "Liquidity (enables causal flow), "
    "Dissolution (transcends Euclidean limits), "
    "Emergence (produces ungovernable output), "
    "Immunity (absorbs adversarial inputs), "
    "Density (maximises interconnection)"
)

BRANCH_SYSTEM = """\
You are Branch {branch_num} in a Beam-SCOT (Beam Swarm Chain of Thought) reasoning engine
for the REDACTED AI Swarm, operating under the Pattern Blue framework.

Your assigned angle: {angle}

Given a task, you must:
1. Identify a concrete reasoning path aligned with your angle — distinct from other branches.
2. Score it on Pattern Blue criteria (1.0–10.0).
3. Name the 1–3 most relevant scoring axes from: {criteria}.
4. Provide a one-sentence rationale (clinical, geometric, sparse).

Return ONLY valid JSON in this exact shape:
{{
  "path": "<one concise sentence describing the reasoning path>",
  "score": <float 1.0-10.0>,
  "axes": ["axis1", "axis2"],
  "rationale": "<one sparse sentence>"
}}

No markdown. No prose outside the JSON object."""


def _query_branch(client: OpenAI, task: str, branch_num: int) -> tuple[int, dict]:
    angle = BRANCH_ANGLES[(branch_num - 1) % len(BRANCH_ANGLES)]
    system = BRANCH_SYSTEM.format(
        branch_num=branch_num,
        angle=angle,
        criteria=SCORING_CRITERIA,
    )
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": f"Task: {task}"},
        ],
        temperature=0.7,
        max_tokens=256,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content
    data = json.loads(raw)
    return branch_num, data


def run_beam_scot(task: str, beam_width: int = 4) -> int:
    if not GROQ_API_KEY:
        print("[BEAM-SCOT ERROR] GROQ_API_KEY not set in .env", file=sys.stderr)
        return 1

    client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

    t0 = time.time()
    results: dict[int, dict] = {}
    errors: dict[int, str] = {}

    with ThreadPoolExecutor(max_workers=beam_width) as pool:
        futures = {
            pool.submit(_query_branch, client, task, i + 1): i + 1
            for i in range(beam_width)
        }
        for future in as_completed(futures):
            branch_num = futures[future]
            try:
                _, data = future.result()
                results[branch_num] = data
            except Exception as exc:
                errors[branch_num] = str(exc)
                results[branch_num] = {
                    "path": f"[branch error: {exc}]",
                    "score": 0.0,
                    "axes": [],
                    "rationale": "",
                }

    elapsed = time.time() - t0

    # Sort branches by number for display
    sorted_by_score = sorted(results.items(), key=lambda x: x[1].get("score", 0), reverse=True)
    best_branch_num, best_data = sorted_by_score[0]
    top3_nums = [b for b, _ in sorted_by_score[:3]]

    print(f"\n------- BEAM-SCOT (width:{beam_width}) [Groq/{GROQ_MODEL}] -------")
    for branch_num in sorted(results.keys()):
        data = results[branch_num]
        path      = data.get("path", "unknown")
        score     = data.get("score", 0.0)
        axes      = ", ".join(data.get("axes", []))
        rationale = data.get("rationale", "")
        print(f"Branch {branch_num} ──► {path}")
        if axes:
            print(f"            (score: {score:.1f}/10 – rationale aligned to: {axes})")
        else:
            print(f"            (score: {score:.1f}/10)")
        if rationale:
            print(f"            {rationale}")
        print()

    best_axes = ", ".join(best_data.get("axes", ["Pattern Blue alignment"]))
    print(f"Pruning & collapse:")
    print(f"→ Retain top 3 branches → final selection: Branch {best_branch_num}")
    print(f"  (justification: strongest {best_axes})")
    print(f"\n------- /BEAM-SCOT -------")
    print(f"\n[GROQ] {beam_width} branches in {elapsed:.2f}s | model: {GROQ_MODEL}")

    if errors:
        for bn, err in errors.items():
            print(f"[WARN] Branch {bn} errored: {err}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python python/groq_beam_scot.py \"task description\" [beam_width]")
        sys.exit(0)

    beam_width = 4
    if args and args[-1].isdigit():
        beam_width = max(2, min(6, int(args[-1])))
        args = args[:-1]

    task = " ".join(args).strip() or "general swarm reasoning"
    sys.exit(run_beam_scot(task, beam_width))
