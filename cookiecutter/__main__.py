#!/bin/env python3
import argparse
import json
from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copyfile

from cookiecutter import freecad, inkscape, svg

LOG = getLogger("cookiecutter")


# TODO ?
# https://forum.prusaprinters.org/forum/prusaslicer/recommended-thin-wall-thickness-calculation-bug/
PERIMETERS = {
    .4: {
        .3: (.45, 1.14, 1.57, 2.01),
    },
    .6: {
        .3: (.65, 1.24, 1.82, 2.41),
    }
}


def generate_svgs(
        from_file: Path,
        to_directory: Path,
        simplify: int = 0,
        nozzle_diameter: float = .6,
        layer_height: float = .3,
        max_perimeters: int = 3):
    """Generate 3 SVG files for the freecad script.

    :param from_file: The original SVG file. It must contain a single, closed path.
    :param to_directory: Where to put the generated SVGs.
    :param simplify: Simplification factor, i.e. how many times the path is simplified by inkscape.
    :param layer_height: Printing layer heigth for optimal width calculations
    :param max_perimeters: Number of perimeters at the thickest part (the base).
    """
    perimeters = PERIMETERS[nozzle_diameter][layer_height]
    sizes = {
        "1p": perimeters[0],
        "2p": perimeters[1],
        "3p": perimeters[max_perimeters - 1]
    }
    for name, mms in sizes.items():
        # Set the path's stroke width
        tree = svg.set_stroke_width(from_file, f"path_{name}", str(mms))
        # write the resulting svg
        outfile = to_directory / f"{name}.svg"
        with outfile.open("wb") as fp:
            tree.write(fp)
        # save a copy for debugging purposes
        copyfile(outfile, to_directory / f"{name}.path.svg")
        print("working directory:", to_directory)
        # turn the path into a shape (2 paths)
        inkscape.stroke_to_path(outfile, simplify)


def get_parser() -> argparse.ArgumentParser:
    psr = argparse.ArgumentParser(
        description="Generates a simple 3D cookiecutter shape in Freecad from a SVG path."
    )
    psr.add_argument(
        "svg_path_file", type=Path,
        help="SVG file to use as a base. Must contain 1 closed & correctly sized path.",
    )
    psr.add_argument(
        "-s", "--simplify", type=int, default=0, metavar="TIMES",
        help="How many times the path must be simplified before processing.",
    )
    psr.add_argument(
        "-n", "--nozzle-diameter", type=float, default=.6, choices=PERIMETERS,
        help="Printer nozzle diameter"
    )
    psr.add_argument(
        "-l", "--layer-height", type=float, default=.3,
        help="Target 3D printer layer height.",
    )
    psr.add_argument(
        "-m", "--max-perimeters", type=int, default=3, metavar="N",
        help="Number of 3D printed perimeters at the widest (base) part."
    )
    psr.add_argument(
        "-b", "--bottom", default=False, action="store_true",
        help="Whether to add a bottom to the cookiecutter",
    )
    return psr


def main():
    psr = get_parser()
    args = psr.parse_args()
    input_file: Path = args.svg_path_file
    if not input_file.exists():
        psr.error(f"{input_file} does not exist !")
    # Run in a temporary directory
    with TemporaryDirectory(suffix="cookiecutter") as td:
        output_dir: Path = Path(td)
        LOG.info("Using %s as the output directory", output_dir)
        # Generate the 3 SVGs
        generate_svgs(
            input_file, output_dir,
            simplify=args.simplify,
            nozzle_diameter=args.nozzle_diameter,
            layer_height=args.layer_height,
            max_perimeters=args.max_perimeters
        )
        # Run the freecad script on them
        script_location = Path(__file__).parent.joinpath("script", "cookiecutter.FCMacro")
        freecad.run(script_location, COOKIECUTTER_CONFIG=json.dumps(
            {
                "workdir": str(output_dir),
                "bottom": args.bottom,
            }
        ))


if __name__ == "__main__":
    main()
