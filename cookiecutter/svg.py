from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

# Register namespaces I empirically found necessary to parse inkscape files
ET.register_namespace('', "http://www.w3.org/2000/svg")
ET.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
ET.register_namespace("cc", "http://creativecommons.org/ns#")


class SVGStyle(dict):
    """Parses and serializes SVG styles in XML attributes"""
    @classmethod
    def parse(cls, raw: str) -> SVGStyle:
        data = {}
        for statement in raw.split(";"):
            key, semicolon, value = statement.partition(":")
            assert semicolon
            data[key] = value
        return cls(data)

    def __str__(self) -> str:
        return ";".join(f"{k}:{v}" for k, v in self.items())


def set_stroke_width(xml_file: Path, path_id: str, width: str) -> ET:
    """Sets path ID and stroke with for the path in the given file"""
    with xml_file.open("rt") as fp:
        tree = ET.parse(fp)
    root = tree.getroot()
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    if not paths:
        raise LookupError("No path found in xml file")
    if len(paths) != 1:
        raise LookupError(f"{xml_file}: 1 path expected, {len(paths)} found")
    path = paths[0]
    style = SVGStyle.parse(path.attrib["style"])
    style["stroke-width"] = width
    path.attrib["style"] = str(style)
    path.attrib["id"] = path_id
    return tree
