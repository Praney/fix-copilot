import xml.etree.ElementTree as ET


def load_tag_names(path: str) -> dict[int, str]:
    # parse file, find <fields> # for each field: int(number) -> name
    root = ET.parse(path).getroot()
    names = {} 
    for field in root.find("fields"):
        names[int(field.attrib["number"])] = field.attrib["name"]  # add one entry to names
    return names


def load_required_fields(path: str) -> dict[str, set[int]]:
    root = ET.parse(path).getroot()
    name_to_tag = {
        field.attrib["name"]: int(field.attrib["number"])
        for field in root.find("fields")
    }
    required = {}
    for message in root.find("messages"):
        required[message.attrib["msgtype"]] = {
            name_to_tag[child.attrib["name"]]
            for child in message
            if child.tag == "field" and child.attrib.get("required") == "Y"
        }
    return required
