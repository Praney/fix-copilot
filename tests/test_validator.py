from fix_tools.validator import check_checksum

HEARTBEAT = "8=FIX.4.4|9=5|35=0|10=163|" 
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
