"""A collection of DEM file functions."""
import math
import os
import shutil
import urllib.request
import zipfile
from .dem_map import getTile

#------------------- Public -------------------

def getDemFromBounds(path, bounds, feedback):
    """Gets a list of the filename of the DEMs intersecting the QgsRectangle."""

    graticules = _getGraticules(bounds)

    feedback.setProgress(0)

    dems = []
    index = 0
    count = len(graticules)
    for item in graticules:
        dem = _downloadDem(path, item)
        # May be null if the tile doesn't exist
        if dem is not None:
            dems.append(dem)

        index = index + 1
        feedback.setProgress(100 * index / count)

    return dems

def getDemFromLayer(path, layer, feedback):
    """Gets a list of the filename of the DEMs intersecting the QgsMapLayer."""
    return getDemFromBounds(path, layer.extent(), feedback)

#------------------- Private -------------------

def _downloadDem(path, graticule):
    """Downloads the DEM file for the specified graticule.

    returns the filename of the DEM, or None if not available.
    """

    name = _getNameFromGraticule(graticule) # The name of the hgt file

    os.makedirs(path, exist_ok=True)

    demName = '%s.hgt' % name
    demPath = os.path.join(path, demName)
    tile = getTile(graticule['lat'], graticule['lng'])

    # It's perfectly possible a tile doesn't exist for this graticule
    if tile:
        _downloadTile(path, tile)

    if os.path.isfile(demPath):
        print('Got %s' % name)
        return demPath

    print('No DEM file available for %s' % name)
    return None

def _downloadTile(path, tile):
    """Downloads the specified tile"""

    uri = tile['uri']
    zipName = os.path.basename(uri)
    zipPath = os.path.join(path, zipName)
    touchFile = os.path.join(path, 'downloaded_%s' % zipName)

    # The touchFile indicates that the tile has previously been downloaded an extracted
    if os.path.isfile(touchFile):
        return

    # Download the tile and extract all the contents into a flat structure
    print('Downloading %s ...' % uri)
    urllib.request.urlretrieve(uri, zipPath)

    with zipfile.ZipFile(zipPath) as zf:
        for item in zf.namelist():
            fileName = os.path.basename(item)

            if not fileName:
                continue

            source = zf.open(item)
            targetPath = os.path.join(path, fileName)

            print('Extracting %s ...' % targetPath)
            target = open(targetPath, 'wb')
            with source, target:
                shutil.copyfileobj(source, target)

        zf.close()

    # Remove the archive to save space and create the touchFile to indicate it's been downloaded
    os.unlink(zipPath)
    open(touchFile, 'a').close()

def _getGraticules(bounds):
    """Gets a list of graticule tuples intersecting the specified QgsRectangle."""

    # Generate the list of all the DEM files needed
    lng0 = math.floor(bounds.xMinimum())
    lat0 = math.floor(bounds.yMinimum())
    lng1 = math.ceil(bounds.xMaximum())
    lat1 = math.ceil(bounds.yMaximum())
    dems = []

    for lng in range(lng0, lng1):
        for lat in range(lat0, lat1):
            dems.append({
                'lat': lat,
                'lng': lng
            })

    return dems

def _getNameFromGraticule(graticule):
    """Gets the name of the DEM for the specified graticule."""

    lat = graticule['lat']
    lng = graticule['lng']

    return '%(lath)s%(lat)02d%(lngh)s%(lng)03d' % {
        'lngh': 'W' if lng < 0 else 'E',
        'lng': abs(lng),
        'lath': 'S' if lat < 0 else 'N',
        'lat': abs(lat)
    }
