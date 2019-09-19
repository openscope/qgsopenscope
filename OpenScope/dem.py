import math
import os
import urllib.request
import zipfile
from qgis.core import QgsRectangle

_DEM_URI = 'http://viewfinderpanoramas.org/dem3/%s.zip'

#------------------- Public -------------------

def getDemFromBounds(path, bounds):
    """Gets a list of the filename of the DEMs intersecting the QgsRectangle."""

    graticules = getGraticules(bounds)

    dems = []
    for item in graticules:
        dem = _downloadDem(path, item)
        # May be null if the tile doesn't exist
        if dem != None:
            dems.append(dem)

    return dems

def getDemFromLayer(path, layer):
    """Gets a list of the filename of the DEMs intersecting the QgsMapLayer."""
    return getDemFromBounds(path, layer.extent())

def getGraticules(bounds):
    """Gets a list of graticule tuples intersecting the specified QgsRectangle."""

    # Generate the list of all the DEM files needed
    x0 = math.floor(bounds.xMinimum())
    y0 = math.floor(bounds.yMinimum())
    x1 = math.ceil(bounds.xMaximum())
    y1 = math.ceil(bounds.yMaximum())
    dems = []

    for x in range(x0, x1):
        for y in range(y0, y1):
            dems.append([x, y])

    return dems

def getGroupFromGraticule(graticule):
    """Gets the name of the group for the specified graticule."""
    
    return '%(hem)s%(row)s%(col)02d' % {
        'hem': 'S' if graticule[1] < 0 else '',
        'row': chr(65 + int(abs(graticule[1] / 4))),
        'col': 1 + (graticule[0] + 180) / 6
    }

def getNameFromGraticule(graticule):
    """Gets the name of the DEM for the specified graticule."""

    return '%(lath)s%(lat)02d%(lngh)s%(lng)03d' % {
        'lngh': 'W' if graticule[0] < 0 else 'E',
        'lng': abs(graticule[0]),
        'lath': 'S' if graticule[1] < 0 else 'N',
        'lat': abs(graticule[1])
    }

#------------------- Private -------------------

def _downloadDem(path, graticule):
    """Downloads the DEM file for the specified graticule.

    returns the filename of the DEM, or None if not available.
    """

    name = getNameFromGraticule(graticule) # The name of the hgt file

    groupName = getGroupFromGraticule(graticule) # The 4x6 degree graticule

    os.makedirs(path, exist_ok=True)

    demName = os.path.join(path, groupName, '%s.hgt' % name)

    # Already exists
    if (os.path.isfile(demName)):
        print('Got %s' % name)
        return demName
    
    # Download the group and extract all the contents
    zipName = os.path.join(path, '%s.zip' % groupName) 
    if not os.path.isfile(zipName):
        uri = _DEM_URI % groupName
        print('Downloading %s.zip...' % groupName)
        urllib.request.urlretrieve(uri, zipName)

        zf = zipfile.ZipFile(zipName)
        print('Unzipping %s...' % zipName)
        for item in zf.namelist():
            zf.extract(item, path)

    if os.path.exists(demName):
        print('Got %s' % name)
        return demName
    else:
        print('No DEM file available for %s' % name)
        return None
