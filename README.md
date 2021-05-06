# slippery

Simple web viewer for raster geodata files.
---

## Installation
Requires
* python3 (tested with 3.9)
* flask
* GDAL
* GDAL python bindings

### To do

* gitignore
* better way to get gdal path
* vector map names?
* load all available vector files automatically
* config.py that abstracts config.json and automatically reloads on change
* read zoom level from config
* read layer extent from files
* inherit layer/group templates to simplify mapview template
* process tiles beginning from low zoom level -> does this even work? base tiles vs overview tiles
* process tiles in the background
* dockerfile

### Notes
* tiling the empty space of VRTs takes a lot of time -> processing them separately is faster for sparse data