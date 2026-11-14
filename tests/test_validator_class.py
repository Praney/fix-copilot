from fix_tools.validator import Validator, compute_checksum

V = Validator({"D": {11, 54}}, {11: "ClOrdID", 54: "Side"})


def build(body: str) -> str:
    head = f"8=FIX.4.4|9={len(body)}|"
    checksum = compute_checksum((head + body).replace("|", "\x01"))
    return f"{head}{body}10={checksum}|"


def test_valid_message_has_no_issues():
    assert V.validate(build("35=D|11=A|54=1|")) == []


def test_reports_missing_required_tag():
    codes = [i.code for i in V.validate(build("35=D|54=1|"))]
    assert codes == ["missing_required_tag"]


def test_structural_and_content_issues_together():
    codes = {i.code for i in V.validate("8=FIX.4.4|9=99|35=D|54=1|10=000|")}
    assert codes == {"bad_body_length", "bad_checksum", "missing_required_tag"}


def test_garbage_does_not_crash_or_duplicate():
    issues = V.validate("not a fix message")
    assert issues != [] and len(issues) == len(set(issues))


def test_from_dictionary_uses_real_spec():
    v = Validator.from_dictionary("data/spec/FIX44.xml")
    codes = [i.code for i in v.validate(build("35=D|54=1|"))]
    assert "missing_required_tag" in codes
