"""A collection of GSHHG file functions."""

import os
import shutil
import urllib.request
import zipfile
from enum import Enum

from qgis.core import QgsFeedback

_GSHHG_VERSION = '2.3.7'
_GSHHG_FILE = 'gshhg-shp-%s.zip' % _GSHHG_VERSION
_GSHHG_URI = 'https://www.ngdc.noaa.gov/mgg/shorelines/data/gshhg/latest/%s' % _GSHHG_FILE

class BorderLevel(Enum):
    """The valid values for the WDBII border levels"""
    NATIONAL = 1
    INTERNAL = 2
    MARITIME = 3

class Resolution(Enum):
    """The valid values for the GSHHG resolution"""
    FULL = 'f'
    HIGH = 'h'
    INTERMEDIATE = 'i'
    LOW = 'l'
    CRUDE = 'c'

class RiverLevel(Enum):
    """The valid values for the WDBII river levels"""
    DOUBLE_LINED_RIVER = 1
    PERMAMENT_MAJOR_RIVER = 2
    ADDITIONAL_MAJOR_RIVER = 3
    ADDITIONAL_RIVER = 4
    MINOR_RIVER = 5
    INTERMITTENT_MAJOR_RIVER = 6
    INTERMITTENT_ADDITIONAL_RIVER = 7
    INTERMITTENT_MINOR_RIVER = 8
    MAJOR_CANAL = 9
    MINOR_CANAL = 10
    IRRIGATION_CANAL = 11

class ShorelineLevel(Enum):
    """The valid values for the GSHHS shoreline levels"""
    CONTINENTAL = 1
    LAKES = 2
    ISLANDS_IN_LAKES = 3
    PONDS = 4
    ANTARCTICA_ICE_FRONT = 5
    ANTARCTICA_GROUND_FRONT = 6

#------------------- Public -------------------

def downloadArchive(path, feedback=QgsFeedback()):
    """Downloads and extracts GSHHG archive to the specified path"""

    os.makedirs(path, exist_ok=True)

    zipPath = os.path.join(path, _GSHHG_FILE)
    touchFile = os.path.join(path, 'downloaded_%s' % _GSHHG_FILE)

    # The touchFile indicates that the tile has previously been downloaded an extracted
    if os.path.isfile(touchFile):
        return

    print('Downloading %s ...' % _GSHHG_URI)
    urllib.request.urlretrieve(
        _GSHHG_URI,
        zipPath,
        lambda count, blockSize, totalSize: _updateDownloadFeedback(feedback, count, blockSize, totalSize)
    )

    print('Extracting %s ...' % zipPath)
    with zipfile.ZipFile(zipPath) as zf:
        zf.extractall(path)
        zf.close()

    # Remove the archive to save space and create the touchFile to indicate it's been downloaded
    os.unlink(zipPath)
    open(touchFile, 'a').close()

    return

def getBorderShapeFile(path, resolution, level, feedback=QgsFeedback()):
    """Returns the path to the WDBII border shapefile"""
    path = _getBorderPath(path, resolution, level)

    if not os.path.exists(path):
        downloadArchive(path, feedback)

    return path

def getRiverShapeFile(path, resolution, level, feedback=QgsFeedback()):
    """Returns the path to the WDBII river shapefile"""
    path = _getRiverPath(path, resolution, level)

    if not os.path.exists(path):
        downloadArchive(path, feedback)

    return path

def getShorelineShapeFile(path, resolution, level, feedback=QgsFeedback()):
    """Returns the path to the WDBII river shapefile"""
    path = _getShorelinePath(path, resolution, level)

    if not os.path.exists(path):
        downloadArchive(path, feedback)

    return path

def migrateArchive(originalPath, newPath):
    """Migrates the GSHHG data to the new path"""

    touchFile = os.path.join(newPath, 'downloaded_%s' % _GSHHG_FILE)

    if os.path.exists(touchFile):
        return

    directories = ['GSHHS_shp', 'WDBII_shp']
    success = False

    for item in directories:
        src = os.path.join(originalPath, item)
        trg = os.path.join(newPath, item)

        try:
            print('Moving {} to {}'.format(src, trg))
            shutil.move(src, trg)
            success = True
        except IOError:
            success = False

    if success:
        open(touchFile, 'a').close()

#------------------- Private -------------------

def _getBorderPath(path, resolution, level):
    """Returns the path to the WDBII border files"""
    shapeFile = 'WDBII_border_{}_L{}.shp'.format(resolution.value, level.value)

    return os.path.join(path, 'WDBII_shp', resolution.value, shapeFile)

def _getRiverPath(path, resolution, level):
    """Returns the path to the WDBII river files"""
    shapeFile = 'WDBII_river_{}_L{:02}.shp'.format(resolution.value, level.value)

    return os.path.join(path, 'WDBII_shp', resolution.value, shapeFile)

def _getShorelinePath(path, resolution, level):
    """Returns the path to the GSHHS shoreline files"""
    shapeFile = 'GSHHS_{}_L{}.shp'.format(resolution.value, level.value)

    return os.path.join(path, 'GSHHS_shp', resolution.value, shapeFile)

def _updateDownloadFeedback(feedback, count, blockSize, totalSize):
    """Updates the specified feedback object"""
    if totalSize == -1:
        progress = 0
    else:
        progress = (count * blockSize) * 100 / totalSize

    feedback.setProgress(min(100, progress))
