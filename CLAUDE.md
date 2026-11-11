# FIX Copilot
Diagnoses FIX protocol failures: deterministic parser/validator tools, RAG over
public specs, an agent (later LangGraph), and evals. Plan: docs/plan.md.
Output contract: docs/contract.md.

## Rules
- Public data only (QuickFIX dictionaries, public specs, synthetic logs).
  Never add proprietary or employer material.
- fix_tools/ is deterministic: no LLM calls in there.
- Write tests first. Run `uv run pytest` and `uv run ruff check .` before finishing.
- One task per session, small diffs, explain design choices briefly.
- Never read data/spec/FIX44.xml in full; query it with Python or grep.
- Teaching mode: I write the core logic (validator, agent loop, LangGraph graph,
  eval metrics); you explain, review and quiz me. Boilerplate is fine to generate.
- Record design decisions in docs/decisions.md.
