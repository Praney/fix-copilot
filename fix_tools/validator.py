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
