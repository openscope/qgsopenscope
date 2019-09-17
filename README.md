# qgsopenscope
A QGIS plugin that adds import/export functions for openScope airports.

## Caveats
**This plugin is in development, and cannot be assumed to be reliable. Use at your own peril!. Always open a blank project before running any of the functions as it will remove any existing layers from the canvas.**

I'm not a Python developer, so please be aware that some of the code may make your eyes bleed.

## Features
* Import geographical features from an openScope airport into a QGIS project.
* Automatically downloads elevation data and generates contours
* Imports shorelines and lakes from the [NOAA GSHHG](https://www.ngdc.noaa.gov/mgg/shorelines/) to generate water polygons
* Generates Airspace, Fix, Map JSON from the project
* Generates GeoJSON terrain files for the airport

#### In development
* Generating Restricted airspace JSON
* Tools for generating circles and extended runway centrelines

## Requirements
* [QGIS 3.4+](https://qgis.org/en/site/) Lower versions of QGIS 3.x may work, haven't been tried.
* The NOAA GSHHG shapefiles. The current (v.2.3.7) version can be [downloaded here](https://www.ngdc.noaa.gov/mgg/shorelines/data/gshhg/latest/gshhg-shp-2.3.7.zip)


## Installation
The plugin can be installed in two ways:
1. Clone this repository and install it from the CLI
2. ~~Download the plugin zip file from releases and install from the QGIS Plugin Manager~~

#### Clone this repository and install it from the CLI
1. You will need python3, PyQt5 and the QGIS dev tools installed.
2. Clone the repository
```git clone https://github.com/openscope/qgsopenscope.git```
3. Make sure pb_tool is install
```python3 -m pip install pb_tool wheel```
3. Deploy the plugin
```pb_tool deploy```

It's advisable to install the experimental QGIS Plugin Reloader plugin. This will enable you to reload the plugin without restarting QGIS ~~if~~ when things go wrong.
