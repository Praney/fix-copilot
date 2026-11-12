# Decisions

## Decision 1: deterministic tools plus LLM reasoning
- Parsing and validation are plain code. The LLM explains and reasons on top.

## Decision 2: dictionary-driven validation plus an overrides layer
- Finding: FIX44.xml marks Symbol (55) inside Instrument as required="N".
- Plan: walk the dictionary, expand components, track `required` at each level,
  then apply data/spec/overrides.yaml for known gaps, each citing the spec.

## Decision 4: validate_message returns every issue, de-duplicated
- One entry point runs all structural checks; the agent never needs to know which exist.
- A real broken message often has several faults (an edited message breaks length and checksum).
- Identical issues (same code and message) are collapsed, keeping first occurrence and order.
- Malformed input is reported as an Issue, never raised.
