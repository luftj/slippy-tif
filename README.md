# slippy-tif

Simple slippy tiles web viewer for raster geodata files.
---

## Installation
Requires
* python3 (tested with 3.9)
* flask
* GDAL
* GDAL python bindings

## Usage

put vector maps (currently only geojson) into ```static/vector_maps/```

add paths to georeferenced raster data to config.json

run ```$ python processing.py``` to convert raster data to tiles

run web server with ```$ python api.py ``` (test server only)

for a production server see e.g. [here](https://flask.palletsprojects.com/en/1.1.x/deploying/index.html).

## dev

### To do

* better way to get gdal path
* handle feature types for vector maps
* different styles for vector maps
* config.py automatically reload on change
* read zoom level from config
* read layer extent from files
* inherit layer/group templates to simplify mapview template
* process tiles beginning from low zoom level -> does this even work? base tiles vs overview tiles
* process tiles continuously in the background
* dockerfile

### Notes
* tiling the empty space of VRTs takes a lot of time -> processing them separately is faster for sparse data