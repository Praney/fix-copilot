from typing import NamedTuple

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
