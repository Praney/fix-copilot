from fix_tools.dictionary import load_tag_names


def test_known_tags_map_to_names():
    names = load_tag_names("data/spec/FIX44.xml")
    assert names[35] == "MsgType" 
    assert names[55] == "Symbol"
    assert names[150] == "ExecType"
def test_keys_are_ints():
    names = load_tag_names("data/spec/FIX44.xml")
    assert all(isinstance(tag, int) for tag in names)
def test_dictionary_is_not_empty():
    assert len(load_tag_names("data/spec/FIX44.xml")) > 500
