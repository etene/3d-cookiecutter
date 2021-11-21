import subprocess
from distutils.spawn import find_executable
from os import environ

FREECAD = find_executable("freecad")
assert FREECAD, "freecad not found in $PATH"


def run(macro: str, **env: str):
    """Starts freecad with the given macro"""
    assert macro.exists()
    subprocess.check_call((FREECAD, str(macro)), env=dict(**environ, **env))
