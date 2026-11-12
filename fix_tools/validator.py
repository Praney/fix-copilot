def compute_checksum(data: str) -> str:
    total = sum(data.encode("latin-1"))
    return f"{total % 256:03d}"
