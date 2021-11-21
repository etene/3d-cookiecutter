# 3d-cookiecutter
Generate 3D printable small cookiecutters from SVG paths.

:warning: Requires Inkscape and Freecad.

## Description

`cookiecutter` processes a file containing a single SVG path in Inkscape to make a small 3d printable cookie cutter shape in Freecad.
The 3d shape is computed based on the printer's nozzle diameter and layer height, so that the cutting side will be 1 perimeter wide.

The original use case is printing small shapes that can cut through a few millimeters of clay to make pendants or earrings.

The script is thus not (yet) adapted for "real" cookie cutters (the ones that cut real cookies); the generated shapes would be too frail for that.

## Usage

To begin, you need a simple SVG file containing 1 closed path, that will be used as the cookiecutter's shape.
That file probably needs to be made with Inkscape, I haven't tested anything else.

Then, call
```
$ python3 -m cookiecutter your_file.svg
```
And wait a bit; the more complex the path, the slower it is. It will fire up Inkscape at some point and is supposed to display the 3D shape if it worked.

If it didn't work, maybe the path is too complex; you can use cookiecutter's `-s/--simplify` switch, that will smoothen the shape a bit before trying to extrude it.  

## Tuning

### Nozzle diameter

The nozzle diameter is .6 mm by default (I should change that). It can be changed with the `-n/--nozzle-diameter` commandline switch.

### Layer height

The only supported layer height for now is .3mm, but that's supposed to change at some point when I'll get to it.
