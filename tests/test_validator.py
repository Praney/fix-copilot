from fix_tools.validator import check_body_length, check_checksum, compute_checksum

HEARTBEAT = "8=FIX.4.4|9=5|35=0|10=163|" 

def test_valid_body_length_returns_none():
    assert check_body_length(HEARTBEAT) is None


def test_wrong_body_length_is_flagged():
    issue = check_body_length("8=FIX.4.4|9=6|35=0|10=163|")
    assert issue.code == "bad_body_length"
    assert "5" in issue.message and "6" in issue.message


def test_missing_body_length_is_flagged():
    assert check_body_length("8=FIX.4.4|35=0|10=163|").code == "missing_body_length"

def test_valid_checksum_returns_none():
    assert check_checksum(HEARTBEAT) is None 

def test_wire_format_with_soh_also_works(): 
    assert check_checksum(HEARTBEAT.replace("|", "\x01")) is None 

def test_edited_message_is_flagged():
    issue = check_checksum("8=FIX.4.4|9=5|35=1|10=163|")
    assert issue.code == "bad_checksum" 
    assert "164" in issue.message and "163" in issue.message 

def test_missing_checksum_is_flagged():
    assert check_checksum("8=FIX.4.4|9=5|35=0|").code == "missing_checksum"


def test_checksum_is_three_digits():
    assert compute_checksum("A") == "065"


def test_checksum_wraps_at_256():
    assert compute_checksum("AAAA") == "004"


def test_checksum_of_empty_is_zero():
    assert compute_checksum("") == "000"


def test_checksum_of_heartbeat():
    assert compute_checksum("8=FIX.4.4\x019=5\x0135=0\x01") == "163"
