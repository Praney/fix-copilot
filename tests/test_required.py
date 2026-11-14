from fix_tools.dictionary import load_required_fields

SAMPLE = """<fix>
<messages>
<message name="Foo" msgtype="Z" msgcat="app">
<field name="A" required="Y"/>
<field name="B" required="N"/>
<component name="C" required="Y"/>
</message>
</messages>
<fields>
<field number="1" name="A" type="STRING"/>
<field number="2" name="B" type="STRING"/>
</fields>
</fix>"""


def test_collects_only_required_direct_fields(tmp_path):
    path = tmp_path / "sample.xml"
    path.write_text(SAMPLE)
    assert load_required_fields(str(path)) == {"Z": {1}}


def test_new_order_single_requirements():
    required = load_required_fields("data/spec/FIX44.xml")
    assert {11, 54}.issubset(required["D"])
    assert 58 not in required["D"]
