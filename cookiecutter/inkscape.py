import subprocess
from distutils.spawn import find_executable
from enum import Enum, auto
from itertools import repeat
from pathlib import Path

INKSCAPE = find_executable("inkscape")
assert INKSCAPE, "inkscape not found in $PATH"


class Verb(str, Enum):
    """An action that can be run by inkscape"""
    EditSelectAll = auto()
    StrokeToPath = auto()
    SelectionSimplify = auto()
    FileSave = auto()


def run(svg_file: Path, *verbs: Verb):
    """Runs inkscape with the given verbs"""
    verbs = ";".join((i.name for i in verbs))
    subprocess.check_call((
        INKSCAPE,  "--batch-process",
        "--verb", verbs, str(svg_file))
    )


def stroke_to_path(svg_file: Path, simplify: int = 0):
    """Turns a stroke object into a path object, simplifying the given number of times."""
    actions: list[Verb] = [
        Verb.EditSelectAll,
        *repeat(Verb.SelectionSimplify, simplify),
        Verb.StrokeToPath, Verb.FileSave,
    ]
    run(svg_file, *actions)
