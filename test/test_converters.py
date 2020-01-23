"""DEM utility tests"""

import unittest
from qgis.core import QgsPointXY

from OpenScope.utilities.converters import fromPointXY, parseCoordinateValue

class ConvertersTest(unittest.TestCase):
    """A collection of tests for the converter fuctions"""

    def testFromPointXY(self):
        """Tests that fromPointXY returns the correct value"""

        point = QgsPointXY(-6.61728333, 4.9468472)
        expected = [
            'N04.94685',
            'W006.61728'
        ]

        self.assertListEqual(fromPointXY(point), expected)

    def testParseCoordinateValue(self):
        """Tests that parseCoordinateValue returns the correct values"""

        self.assertEqual(parseCoordinateValue(-1.234), -1.234)
        self.assertEqual(parseCoordinateValue(171.123), 171.123)
        self.assertEqual(parseCoordinateValue('N47.83333330'), 47.8333333)
        self.assertEqual(parseCoordinateValue('S1.10'), -1.1)
        self.assertEqual(parseCoordinateValue('W122.43465440'), -122.43465440)
        self.assertEqual(parseCoordinateValue('E22.237654'), 22.237654)
        self.assertAlmostEqual(parseCoordinateValue('N40d56.811'), 40.94685)
        self.assertAlmostEqual(parseCoordinateValue('W076d37.037'), -76.61728333)
        self.assertAlmostEqual(parseCoordinateValue('N40d56m48.65'), 40.9468472)
        self.assertAlmostEqual(parseCoordinateValue('W076d37m02.20'), -76.6172778)

        self.assertRaises(Exception, parseCoordinateValue, -181)
        self.assertRaises(Exception, parseCoordinateValue, 181)
