SOH = "\x01"


def split_fields(raw: str) -> list[tuple[int, str]]:
    raw = raw.strip()
    delimiter = SOH if SOH in raw else "|"
    fields = []
    for piece in raw.split(delimiter):
        if not piece:
            continue
        tag, sep, value = piece.partition("=")
        if not sep or not (tag.isascii() and tag.isdigit()):
            raise ValueError(f"Malformed FIX field: {piece!r}")
        fields.append((int(tag), value))
    return fields
