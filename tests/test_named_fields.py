import pytest

from fix_tools.parser import Field, parse

NAMES = {8: "BeginString", 35: "MsgType"}


def test_adds_names():
    assert parse("8=FIX.4.4|35=A|", NAMES) == [
        Field(8, "BeginString", "FIX.4.4"),
        Field(35, "MsgType", "A"),
    ]


def test_unknown_tag_has_no_name():
    assert parse("9999=x|", NAMES) == [Field(9999, None, "x")]


def test_malformed_still_raises():
    with pytest.raises(ValueError):
        parse("35A|", NAMES)
