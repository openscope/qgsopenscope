"""DEM utility tests"""

#pylint: disable=line-too-long

import unittest

from OpenScope.utilities.gshhg import _getBorderPath, _getShorelinePath, _getRiverPath, BorderLevel, Resolution, RiverLevel, ShorelineLevel

class GshhgTest(unittest.TestCase):
    """A collection of tests for the GSHHG fuctions"""

    def testGetBorderPath(self):
        """Test that _getBorderPath returns the correct value"""
        path = './'

        self.assertEqual(_getBorderPath(path, Resolution.FULL, BorderLevel.NATIONAL), './WDBII_shp/f/WDBII_border_f_L1.shp')
        self.assertEqual(_getBorderPath(path, Resolution.HIGH, BorderLevel.INTERNAL), './WDBII_shp/h/WDBII_border_h_L2.shp')
        self.assertEqual(_getBorderPath(path, Resolution.INTERMEDIATE, BorderLevel.MARITIME), './WDBII_shp/i/WDBII_border_i_L3.shp')
        self.assertEqual(_getBorderPath(path, Resolution.LOW, BorderLevel.MARITIME), './WDBII_shp/l/WDBII_border_l_L3.shp')
        self.assertEqual(_getBorderPath(path, Resolution.CRUDE, BorderLevel.MARITIME), './WDBII_shp/c/WDBII_border_c_L3.shp')

    def testGetRiverPath(self):
        """Test that _getRiverPath returns the correct value"""
        path = './'

        self.assertEqual(_getRiverPath(path, Resolution.FULL, RiverLevel.DOUBLE_LINED_RIVER), './WDBII_shp/f/WDBII_river_f_L01.shp')
        self.assertEqual(_getRiverPath(path, Resolution.HIGH, RiverLevel.PERMAMENT_MAJOR_RIVER), './WDBII_shp/h/WDBII_river_h_L02.shp')
        self.assertEqual(_getRiverPath(path, Resolution.INTERMEDIATE, RiverLevel.ADDITIONAL_MAJOR_RIVER), './WDBII_shp/i/WDBII_river_i_L03.shp')
        self.assertEqual(_getRiverPath(path, Resolution.LOW, RiverLevel.ADDITIONAL_RIVER), './WDBII_shp/l/WDBII_river_l_L04.shp')
        self.assertEqual(_getRiverPath(path, Resolution.CRUDE, RiverLevel.MINOR_RIVER), './WDBII_shp/c/WDBII_river_c_L05.shp')
        self.assertEqual(_getRiverPath(path, Resolution.CRUDE, RiverLevel.INTERMITTENT_MAJOR_RIVER), './WDBII_shp/c/WDBII_river_c_L06.shp')
        self.assertEqual(_getRiverPath(path, Resolution.CRUDE, RiverLevel.INTERMITTENT_ADDITIONAL_RIVER), './WDBII_shp/c/WDBII_river_c_L07.shp')
        self.assertEqual(_getRiverPath(path, Resolution.CRUDE, RiverLevel.INTERMITTENT_MINOR_RIVER), './WDBII_shp/c/WDBII_river_c_L08.shp')
        self.assertEqual(_getRiverPath(path, Resolution.CRUDE, RiverLevel.MAJOR_CANAL), './WDBII_shp/c/WDBII_river_c_L09.shp')
        self.assertEqual(_getRiverPath(path, Resolution.CRUDE, RiverLevel.MINOR_CANAL), './WDBII_shp/c/WDBII_river_c_L10.shp')
        self.assertEqual(_getRiverPath(path, Resolution.CRUDE, RiverLevel.IRRIGATION_CANAL), './WDBII_shp/c/WDBII_river_c_L11.shp')

    def testGetShorelinePath(self):
        """Test that _getShorelinePath returns the correct value"""
        path = './'

        self.assertEqual(_getShorelinePath(path, Resolution.FULL, ShorelineLevel.CONTINENTAL), './GSHHS_shp/f/GSHHS_f_L1.shp')
        self.assertEqual(_getShorelinePath(path, Resolution.HIGH, ShorelineLevel.LAKES), './GSHHS_shp/h/GSHHS_h_L2.shp')
        self.assertEqual(_getShorelinePath(path, Resolution.INTERMEDIATE, ShorelineLevel.ISLANDS_IN_LAKES), './GSHHS_shp/i/GSHHS_i_L3.shp')
        self.assertEqual(_getShorelinePath(path, Resolution.LOW, ShorelineLevel.PONDS), './GSHHS_shp/l/GSHHS_l_L4.shp')
        self.assertEqual(_getShorelinePath(path, Resolution.CRUDE, ShorelineLevel.ANTARCTICA_ICE_FRONT), './GSHHS_shp/c/GSHHS_c_L5.shp')
        self.assertEqual(_getShorelinePath(path, Resolution.CRUDE, ShorelineLevel.ANTARCTICA_GROUND_FRONT), './GSHHS_shp/c/GSHHS_c_L6.shp')
