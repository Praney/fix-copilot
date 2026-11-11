# Decisions

## Decision 1: deterministic tools plus LLM reasoning
- Parsing and validation are plain code. The LLM explains and reasons on top.

## Decision 2: dictionary-driven validation plus an overrides layer
- Finding: FIX44.xml marks Symbol (55) inside Instrument as required="N".
- Plan: walk the dictionary, expand components, track `required` at each level,
  then apply data/spec/overrides.yaml for known gaps, each citing the spec.
