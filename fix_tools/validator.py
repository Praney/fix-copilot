from typing import NamedTuple

from fix_tools.parser import split_fields

SOH = "\x01"


class Issue(NamedTuple):
    code: str
    message: str


def compute_checksum(data: str) -> str:
    total = sum(data.encode("latin-1"))
    return f"{total % 256:03d}"


def check_checksum(raw: str) -> Issue | None:
    raw = raw.strip()
    if SOH not in raw:
        raw = raw.replace("|", SOH)
    marker = SOH + "10="
    idx = raw.rfind(marker)
    if idx == -1:
        return Issue("missing_checksum", "No CheckSum (10) field found")
    data = raw[: idx + 1]
    claimed = raw[idx + len(marker):].split(SOH, 1)[0]
    expected = compute_checksum(data)
    if claimed != expected:
        return Issue("bad_checksum", f"expected {expected}, message says {claimed}")
    return None


def check_body_length(raw: str) -> Issue | None:
    raw = raw.strip()
    if SOH not in raw:
        raw = raw.replace("|", SOH)
    marker = SOH + "9="
    idx = raw.find(marker)
    if idx == -1:
        return Issue("missing_body_length", "No BodyLength (9) field found")
    value_start = idx + len(marker)
    value_end = raw.find(SOH, value_start)
    if value_end == -1:
        return Issue("bad_body_length", "BodyLength (9) field is not terminated")
    claimed = raw[value_start:value_end]
    if not (claimed.isascii() and claimed.isdigit()):
        return Issue("bad_body_length", f"BodyLength is not a number: {claimed!r}")
    checksum_idx = raw.rfind(SOH + "10=")
    if checksum_idx == -1:
        return Issue("missing_checksum", "No CheckSum (10) field found")
    actual = (checksum_idx + 1) - (value_end + 1)
    if actual != int(claimed):
        return Issue("bad_body_length", f"expected {actual}, message says {claimed}")
    return None


def check_field_order(raw: str) -> Issue | None:
    try:
        tags = [tag for tag, _ in split_fields(raw)]
    except ValueError as exc:
        return Issue("malformed_message", str(exc))
    if tags[:3] != [8, 9, 35]:
        return Issue(
            "bad_field_order",
            f"BeginString (8), BodyLength (9), MsgType (35) must come first, found {tags[:3]}",
        )
    if tags[-1:] != [10]:
        return Issue(
            "bad_field_order",
            f"CheckSum (10) must be the last field, found {tags[-1:]}",
        )
    return None


def validate_message(raw: str) -> list[Issue]:
    results = (
        check_field_order(raw),
        check_checksum(raw),
        check_body_length(raw),
    )
    issues = [issue for issue in results if issue is not None]
    return list(dict.fromkeys(issues))


def check_required_fields(
    raw: str, required: dict[str, set[int]], tag_names: dict[int, str]
) -> Issue | None:
    try:
        fields = split_fields(raw)
    except ValueError as exc:
        return Issue("malformed_message", str(exc))
    present = {tag for tag, _ in fields}
    msgtype = next((value for tag, value in fields if tag == 35), None)
    if msgtype is None:
        return Issue("missing_msg_type", "No MsgType (35) field found")
    if msgtype not in required:
        return Issue("unknown_msg_type", f"Unknown MsgType (35): {msgtype!r}")
    missing = sorted(required[msgtype] - present)
    if not missing:
        return None
    listed = ", ".join(f"{tag} ({tag_names.get(tag, '?')})" for tag in missing)
    return Issue("missing_required_tag", f"{msgtype} is missing: {listed}")


