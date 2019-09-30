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
2. Download the plugin zip file from releases and install from the QGIS Plugin Manager

#### Clone this repository and install it from the CLI
These instructions are for Ubuntu Linux, modify accordingly depending on your distro of choice.

##### Install QGIS 3.4
If you don't have QGIS installed, you can use [instructions provided](https://qgis.org/en/site/forusers/download.html). The plugin has been developed on 3.4 Madeira (LTR). Add the following file to `/etc/apt/sources.list.d/`. eg. for Ubuntu 18.03 (Bionic Beaver):
```
# /etc/apt/sources.list.d/qgis.list
deb     https://qgis.org/ubuntu-ltr bionic main
deb-src https://qgis.org/ubuntu-ltr bionic main
```

Update the packages and install
``` bash
# Add the key, as provided by the QGIS instructions
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key <KEY>

# Update the packages
sudo apt-get update

# Install the required packages
sudo apt-get install qgis
```

##### Configure the environment
Install prerequisites
``` bash
sudo apt-get install git python3-pip python3-setuptools pyqt5-dev-tools

python3 -m pip install wheel pb_tool
```
Make sure `~/.local/bin` is in your PATH variable, as that is where pb_tool is located
``` bash
export PATH=$PATH:~/.local/bin
```

Enter the plugin directory and deploy.
``` bash
# Deploy expects the plugins directory to exist, so the first time
mkdir -p ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins

pb_tool deploy
```

It's advisable to install the experimental QGIS Plugin Reloader plugin. This will enable you to reload the plugin without restarting QGIS ~~if~~ when things go wrong.

## Usage
Before using the plugin, the GSHHG shapefiles need to be downloaded and extracted. The plugin only uses files in the `GSHHS_shp/f` directory.

Once the plugin has been installed, it can be found in the `Plugins` menu.
1. Configure the plugin settings, making sure the GSHHS path is configured:
Plugins -> QgsOpenScope -> QgsOpenScope
2. Select Plugins -> QgsOpenScope -> Load Aiport
3. Select the airport file you want to load
This will load all the layers from the `airport.json` file
3. Generate the terrain:
Plugins -> QgsOpenScope -> Generate Terrain
4. Select the airport file for which the terrain will be generated
Click OK, and wait. The plugin may take several minutes to run, depending on your internet connection and hardware

Exporting data can also be done.@
* Simply use the Export ... option and it will copy the generated JSON to the clipboard
* Terrain is exported by selecting which terrain layers you want, and using the Export function. It will ask you where you want to save the GeoJSON file
