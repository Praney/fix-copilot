from fix_tools.validator import compute_checksum


def test_checksum_is_three_digits():
    assert compute_checksum("A") == "065"


def test_checksum_wraps_at_256():
    assert compute_checksum("AAAA") == "004"


def test_checksum_of_empty_is_zero():
    assert compute_checksum("") == "000"
