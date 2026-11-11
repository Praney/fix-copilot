import xml.etree.ElementTree as ET


def load_tag_names(path: str) -> dict[int, str]:
    # parse file, find <fields> # for each field: int(number) -> name
    root = ET.parse(path).getroot()
    names = {} 
    for field in root.find("fields"):
        names[int(field.attrib["number"])] = field.attrib["name"]  # add one entry to names
    return names
