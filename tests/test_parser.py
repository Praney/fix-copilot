import pytest

from fix_tools.parser import split_fields


def test_splits_pipe_delimited():
    assert split_fields("8=FIX.4.4|35=A|98=0|") == [
        (8, "FIX.4.4"), (35, "A"), (98, "0"),
    ]


def test_splits_soh_delimited():
    assert split_fields("8=FIX.4.4\x0135=A\x01") == [(8, "FIX.4.4"), (35, "A")]


def test_keeps_order_and_duplicates():
    assert split_fields("453=2|448=A|448=B|") == [(453, "2"), (448, "A"), (448, "B")]


def test_value_may_contain_equals():
    assert split_fields("58=a=b|") == [(58, "a=b")]


@pytest.mark.parametrize("raw", ["35A|", "abc=1|", "=5|"])
def test_malformed_raises(raw):
    with pytest.raises(ValueError):
        split_fields(raw)

def test_ignores_surrounding_whitespace():
    assert split_fields("8=FIX.4.4|35=A|\n") == [(8, "FIX.4.4"), (35, "A")]
