"""DEM utility tests"""

import unittest
from qgis.core import QgsFeature, QgsGeometry, QgsPointXY

from OpenScope.utilities.converters import fromPointXY, fromPolygon, fromPolyline, parseCoordinateValue, toPointXY

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

    def testFromPolygon(self):
        """Test that fromPolyline returns the correct value"""

        #pylint: disable=line-too-long
        wkt = 'Polygon ((-71.5552857013641983 -54.53569639563289684, -70.99220858847313309 -55.20906696362634136, -70.60327903627002399 -54.44281769659932024, -70.99220858847313309 -54.169986518188189, -71.5552857013641983 -54.53569639563289684))'
        expected = [
            ['S54.53570', 'W071.55529'],
            ['S55.20907', 'W070.99221'],
            ['S54.44282', 'W070.60328'],
            ['S54.16999', 'W070.99221']
        ]

        feature = QgsFeature()
        geom = QgsGeometry.fromWkt(wkt)
        feature.setGeometry(geom)

        points = fromPolygon(feature)

        self.assertListEqual(points, expected)

    def testFromPolyline(self):
        """Test that fromPolyline returns the correct value"""

        #pylint: disable=line-too-long
        wkt = 'LineString (-70.60327903627002399 -54.44281769659932024, -70.99220858847313309 -55.20906696362634136, -71.5552857013641983 -54.53569639563289684, -70.99220858847313309 -54.169986518188189, -70.60327903627002399 -54.44281769659932024)'
        expected = [
            ['S54.44282', 'W070.60328', 'S55.20907', 'W070.99221'],
            ['S55.20907', 'W070.99221', 'S54.53570', 'W071.55529'],
            ['S54.53570', 'W071.55529', 'S54.16999', 'W070.99221'],
            ['S54.16999', 'W070.99221', 'S54.44282', 'W070.60328']
        ]

        feature = QgsFeature()
        geom = QgsGeometry.fromWkt(wkt)
        feature.setGeometry(geom)

        points = fromPolyline(feature)

        self.assertListEqual(points, expected)

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

    def testToPointXY(self):
        """Tests that toPointXY returns the correct value"""

        value = [
            'N04.94685',
            'W006.61728'
        ]
        expected = QgsPointXY(-6.61728, 4.94685)

        point = toPointXY(value)

        self.assertEqual(point.x(), expected.x())
        self.assertEqual(point.y(), expected.y())
