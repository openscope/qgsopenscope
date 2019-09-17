import math
import os
import urllib.request
import zipfile
from qgis.core import QgsRectangle

DEM_URI = 'http://viewfinderpanoramas.org/dem3/%s.zip'

def get_dem(path, graticule):
    name = get_name_from_graticule(graticule) # The name of the hgt file

    groupName = get_group_from_graticule(graticule) # The 4x6 degree graticule

    os.makedirs(path, exist_ok=True)

    demName = os.path.join(path, groupName, '%s.hgt' % name)

    # Already exists
    if (os.path.isfile(demName)):
        print('Got %s' % name)
        return demName
    
    # Download the group and extract all the contents
    zipName = os.path.join(path, '%s.zip' % groupName) 
    if not os.path.isfile(zipName):
        uri = DEM_URI % groupName
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

def get_dem_from_layer(path, layer):
    # Get the bounding box of all the features
    bounds = layer.extent()

    graticules = get_graticules(bounds)

    dems = []
    for item in graticules:
        dem = get_dem(path, item)
        # May be null if the tile doesn't exist
        if dem != None:
            dems.append(dem)

    return dems

def get_graticules(bounds):
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

def get_group_from_graticule(graticule):
    return '%(hem)s%(row)s%(col)02d' % {
        'hem': 'S' if graticule[1] < 0 else '',
        'row': chr(65 + int(abs(graticule[1] / 4))),
        'col': 1 + (graticule[0] + 180) / 6
    }

def get_name_from_graticule(graticule):
    return '%(lath)s%(lat)02d%(lngh)s%(lng)03d' % {
        'lngh': 'W' if graticule[0] < 0 else 'E',
        'lng': abs(graticule[0]),
        'lath': 'S' if graticule[1] < 0 else 'N',
        'lat': abs(graticule[1])
    }
