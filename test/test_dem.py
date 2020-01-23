"""DEM utility tests"""

import unittest
from qgis.core import QgsRectangle

from OpenScope.utilities.dem import _getGraticules, _getNameFromGraticule
from OpenScope.utilities.dem_map import getTile

class DemTest(unittest.TestCase):
    """A collection of tests for the DEM fuctions"""

    def testDemExists(self):
        """Test that the correct DEM file is found"""

        # EINN - Shannon Airport
        lat = 52.699124
        lng = -8.914895
        expected = {
            'lat0': 52,
            'lng0': -12,
            'lat1': 56,
            'lng1': -6,
            'area': 24,
            'uri': 'http://viewfinderpanoramas.org/dem3/N29.zip',
            'name': 'N29'
        }

        tile = getTile(lat, lng)

        self.assertDictEqual(tile, expected)

    def testDemNotExists(self):
        """Test that a null tile is returned when expected"""

        # Atlantic Ocean, west of EINN
        lat = 52.699124
        lng = -20

        tile = getTile(lat, lng)

        self.assertIsNone(tile)

    def testDemSmallestTile(self):
        """Test that the smallest tile is returned when an ambiguous match is found"""

        # Coronation Island
        lat = -60.691727
        lng = -45.455254
        expected = {
            'lat0': -64,
            'lng0': -48,
            'lat1': -60,
            'lng1': -42,
            'area': 24,
            'uri': 'http://viewfinderpanoramas.org/dem3/SP23.zip',
            'name': 'SP23'
        }

        tile = getTile(lat, lng)

        self.assertDictEqual(tile, expected)

    def testGetGraticule(self):
        """Tests that _getGraticules returns the correct array"""

        # EINN - Shannon Airport
        bounds = QgsRectangle(-0.5, -0.5, 0.5, 0.5)
        expected = [
            {'lng': -1, 'lat': -1},
            {'lng': -1, 'lat': 0},
            {'lng': 0, 'lat': -1},
            {'lng': 0, 'lat': 0},
        ]

        graticules = _getGraticules(bounds)

        self.assertListEqual(graticules, expected)

    def testGetNameFromGraticule(self):
        """Tests that _getNameFromGraticule returns the correct string"""

        self.assertEqual(_getNameFromGraticule({'lat': -1, 'lng': -1}), 'S01W001')
        self.assertEqual(_getNameFromGraticule({'lat': -89, 'lng': 57}), 'S89E057')
        self.assertEqual(_getNameFromGraticule({'lat': 3, 'lng': -123}), 'N03W123')
        self.assertEqual(_getNameFromGraticule({'lat': 75, 'lng': 179}), 'N75E179')
