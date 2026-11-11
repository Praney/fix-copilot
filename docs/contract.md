# Contract
Input: {"fix_version": "FIX.4.4", "messages": ["8=FIX.4.4|9=...|35=5|..."], "context": "optional"}
Output: {"category", "summary", "root_cause", "evidence": [{"msg_index", "tags": []}],
"spec_citations": [], "suggested_fix": [], "confidence", "needs_more_info": []}
Categories: sequence_too_low, sequence_gap, bad_checksum, bad_body_length,
missing_required_tag, invalid_enum, order_reject, session_reject, business_reject,
duplicate_clordid, heartbeat_timeout, insufficient_evidence
