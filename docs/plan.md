# Plan
Problem: given raw FIX messages, explain what went wrong, name the root cause, cite
the spec and suggest a fix. It must be able to say "insufficient evidence".
v1 scope: FIX 4.4, one synthetic venue, session and order-level failures.

Weeks (8-10 h/week):
1-2 parser, validator, session tracker, 10 scenarios, CI
3 LLM baseline and eval v0
4-5 RAG (pgvector, hybrid search, reranker, citations)
6 tool-using agent, no framework
7-8 LangGraph and MCP, human approval step
9-10 Hugging Face LoRA classifier
11 evals in CI, tracing, guardrails
12 demo, README, results table
