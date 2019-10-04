"""The terrain generator."""
import os
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from qgis.core import (
    QgsFeature, QgsFeatureRequest, QgsField,
    QgsGeometry,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsWkbTypes
)
import processing # pylint: disable=import-error
from .GeneratorBase import GeneratorBase, GeneratorConfigBase
from .dem import getDemFromLayer

_MEMORY_OUTPUT = 'memory:'

class TerrainGeneratorConfig(GeneratorConfigBase):
    """The configuration options passed to the TerrainGenerator constructor."""

    contourInterval = 304.8

    gshhsPath = None

class TerrainGenerator(GeneratorBase):
    """The terrain generator."""

#------------------- Public -------------------

    def generateTerrain(self, feedback=None):
        """Generates the terrain"""

        terrain = TerrainGenerator._getTerrainGroup()

        if terrain:
            for layer in terrain.findLayers():
                terrain.removeLayer(layer.layer())
        else:
            terrain = self.addGroup('Terrain')

        polygons = self._getSelectedPolygons()

        if not polygons:
            return (False, 'No valid polygons were selected to determine the terrain bounds')

        self._generateTerrain(terrain, polygons, feedback)

        return (True, None)

    @staticmethod
    def hasExistingLayers():
        """Gets a flag indicating whether there are existing terrain layers"""
        group = TerrainGenerator._getTerrainGroup()
        return group is not None and group.findLayers() != []

#------------------- Private -------------------

    def _generateTerrain(self, group, polygons, feedback):
        """Generate the terrain."""
        # Get the clipping bounds
        bounds, perimeter, buffer = self._getPerimeter(polygons)
        # self._addLayerToGroup(airspace, group)
        # self._addLayerToGroup(perimeter, group)
        # self._addLayerToGroup(buffer, group)

        # Get the water
        water = self._getWater(bounds, buffer)
        self.addLayerToGroup(water, group)

        # Height data
        mergedDem, clippedDem, contours = self._getElevationData(buffer, feedback)
        # self._addLayerToGroup(mergedDem, group)
        # self._addLayerToGroup(clippedDem, group)
        # self._addLayerToGroup(contours, group)

        # Clean the contours
        cleaned = self._getCleanContours(contours, perimeter, bounds)
        self.addLayerToGroup(cleaned, group)

        # Normalize the contours
        self._normalizeContours(cleaned, clippedDem)

        # Clean up unused layers
        for l in [mergedDem, clippedDem, contours]:
            del l

    def _getBounds(self, polygons):
        """Gets the bounds for the terrain"""

        bounds = self.createMemoryLayer('Bounds', 'Polygon')
        geometry = None

        for item in polygons:
            geom = QgsGeometry.fromPolygonXY(item.geometry().asPolygon())
            if geometry:
                geometry = geometry.combine(geom)
            else:
                geometry = geom

        feature = QgsFeature()
        feature.setGeometry(geometry)
        bounds.dataProvider().addFeatures([feature])

        return bounds

    def _getCleanContours(self, contours, perimeter, airspace):
        """Get the cleaned contours."""
        # Simplify the contours
        result = processing.run('qgis:simplifygeometries', {
            'INPUT': contours,
            'TOLERANCE': 0.002,
            'OUTPUT': _MEMORY_OUTPUT
        })
        simplified = result['OUTPUT']
        simplified.setName('Contours - Simplified')

        # Merge with perimeter
        result = processing.run('qgis:mergevectorlayers', {
            'LAYERS': [simplified, perimeter],
            'OUTPUT': _MEMORY_OUTPUT
        })
        merged = result['OUTPUT']
        merged.setName('Contours - Merged')

        # Polygonise
        result = processing.run('qgis:polygonize', {
            'INPUT': merged,
            'OUTPUT': _MEMORY_OUTPUT,
        })
        polygons = result['OUTPUT']
        polygons.setName('Contours - Polygons')

        # Select all polygons smaller than 0.0005 sq degrees (about 38ha at lat=52))
        # and eliminate them
        selection = polygons.getFeatures(QgsFeatureRequest().setFilterExpression('$area < 0.00005'))
        polygons.selectByIds([k.id() for k in selection])

        result = processing.run('qgis:eliminateselectedpolygons', {
            'INPUT': polygons,
            'OUTPUT': _MEMORY_OUTPUT,
            'MODE': 2 # Largest common boundary
        })
        cleaned = result['OUTPUT']
        cleaned.setName('Contours - Cleaned')

        # Delete any features that weren't eliminated (outside a common boundary)
        selection = cleaned.getFeatures(QgsFeatureRequest().setFilterExpression('$area < 0.00005'))
        cleaned.dataProvider().deleteFeatures([k.id() for k in selection])

        # Clip to airspace
        result = processing.run('qgis:clip', {
            'INPUT': cleaned,
            'OUTPUT': _MEMORY_OUTPUT,
            'OVERLAY': airspace
        })
        clipped = result['OUTPUT']
        clipped.setName('Contours - Clipped')

        # Multipart to single part
        result = processing.run('qgis:multiparttosingleparts', {
            'INPUT': clipped,
            'OUTPUT': _MEMORY_OUTPUT
        })
        final = result['OUTPUT']
        final.setName('Contours - Final')

        # Styling
        final.renderer().symbol().setColor(QColor.fromRgb(0xff, 0x9e, 0x17))

        return final

    def _getContourInterval(self):
        """Get the contour interval (in metres)."""
        return self._config.contourInterval

    def _getElevationData(self, boundingLayer, feedback):
        """Get the elevation layers."""
        demFiles = getDemFromLayer(self.getDemsPath(), boundingLayer)

        airportPath = self.getAirportPath()

        # Merge all the DEM files into a single geotiff
        mergedFile = os.path.join(airportPath, 'Elevation - Merged.tif')
        if os.path.isfile(mergedFile):
            os.unlink(mergedFile)

        result = processing.run('gdal:merge', {
            'INPUT': demFiles,
            'DATA_TYPE': 1,
            'OUTPUT': mergedFile
        }, feedback)
        merged = QgsRasterLayer(result['OUTPUT'], 'Elevation - Merged')

        # Clip the DEM file to the bounds
        clippedFile = os.path.join(airportPath, 'Elevation - Clipped.tif')
        if os.path.isfile(clippedFile):
            os.unlink(clippedFile)

        result = processing.run('gdal:cliprasterbymasklayer', {
            'INPUT': mergedFile,
            'MASK': boundingLayer,
            'OUTPUT': clippedFile
        }, feedback)
        clipped = QgsRasterLayer(result['OUTPUT'], 'Elevation - Clipped')

        # Generate the contours
        contourFile = os.path.join(airportPath, 'Contours.shp')
        if os.path.isfile(contourFile):
            os.unlink(contourFile)

        result = processing.run('gdal:contour', {
            'INPUT': clippedFile,
            'BAND' : 1,
            'INTERVAL': self._getContourInterval(),
            'OUTPUT': contourFile
        })
        contours = QgsVectorLayer(result['OUTPUT'], 'Contours')

        return (merged, clipped, contours)

    def _getPerimeter(self, polygons):
        """Gets the perimeter for the terrain"""

        bounds = self._getBounds(polygons)

        # Perimeter
        result = processing.run('qgis:polygonstolines', {
            'INPUT': bounds,
            'OUTPUT': _MEMORY_OUTPUT
        })
        perimeter = result['OUTPUT']
        perimeter.setName('Perimeter')

        # Buffer the airspace
        result = processing.run('qgis:buffer', {
            'INPUT': bounds,
            'OUTPUT': _MEMORY_OUTPUT,
            'DISTANCE': 0.005
        })
        buffer = result['OUTPUT']
        buffer.setName('Buffer')

        return (bounds, perimeter, buffer)

    def _getSelectedPolygons(self):
        """Gets the list of selected polygons"""

        selected = []

        for layer in QgsProject.instance().layerTreeRoot().findLayers():
            features = filter(
                lambda x: x.geometry().type() == QgsWkbTypes.PolygonGeometry,
                layer.layer().selectedFeatures()
            )

            selected.extend(features)

        return selected

    @staticmethod
    def _getTerrainGroup():
        """Gets the terrain group"""
        return QgsProject.instance().layerTreeRoot().findGroup('Terrain')

    def _getWater(self, airspace, buffer):
        """Get the water layer."""
        gshhsPath = self._config.gshhsPath

        coastlines = QgsVectorLayer(os.path.join(gshhsPath, 'GSHHS_shp/f/GSHHS_f_L1.shp'), 'Coastline')
        lakes = QgsVectorLayer(os.path.join(gshhsPath, 'GSHHS_shp/f/GSHHS_f_L2.shp'), 'Lakes')

        # Clip by the buffer
        result = processing.run('qgis:clip', {
            'INPUT': coastlines,
            'OVERLAY': buffer,
            'OUTPUT': _MEMORY_OUTPUT
        })
        clipped_coastlines = result['OUTPUT']

        result = processing.run('qgis:clip', {
            'INPUT': lakes,
            'OVERLAY': buffer,
            'OUTPUT': _MEMORY_OUTPUT
        })
        clipped_lakes = result['OUTPUT']

        # Simplify
        result = processing.run('qgis:simplifygeometries', {
            'INPUT': clipped_coastlines,
            'TOLERANCE': 0.002,
            'OUTPUT': _MEMORY_OUTPUT
        })
        cleaned = result['OUTPUT']

        # Delete any small islands
        it = cleaned.getFeatures(QgsFeatureRequest().setFilterExpression("$area < 0.0005"))
        cleaned.dataProvider().deleteFeatures([i.id() for i in it])

        # Invert to get the water
        result = processing.run('qgis:difference', {
            'INPUT': buffer,
            'OVERLAY': cleaned,
            'OUTPUT': _MEMORY_OUTPUT
        })
        difference = result['OUTPUT']

        # Merge sea with lakes
        result = processing.run('qgis:mergevectorlayers', {
            'LAYERS': [difference, clipped_lakes],
            'OUTPUT': _MEMORY_OUTPUT
        })
        merged_water = result['OUTPUT']

        # Re-clip by the airspace
        result = processing.run('qgis:clip', {
            'INPUT': merged_water,
            'OVERLAY': airspace,
            'OUTPUT': _MEMORY_OUTPUT
        })
        clipped = result['OUTPUT']

        # Multipart to single part
        result = processing.run('qgis:multiparttosingleparts', {
            'INPUT': clipped,
            'OUTPUT': _MEMORY_OUTPUT
        })
        water = result['OUTPUT']
        water.setName('Water')

        # Delete any small area of water
        it = water.getFeatures(QgsFeatureRequest().setFilterExpression("$area < 0.0005"))
        water.dataProvider().deleteFeatures([i.id() for i in it])

        # Add an elevation attribute (0)
        water.startEditing()
        water.addAttribute(QgsField("elevation", QVariant.Double))
        elevationIndex = water.fields().indexFromName('elevation')
        for f in water.getFeatures():
            f[elevationIndex] = 0
            water.updateFeature(f)
        water.commitChanges()

        # Styling
        water.renderer().symbol().setColor(QColor.fromRgb(0x00, 0xff, 0xff))

        return water

    def _normalizeContours(self, contours, elevation):
        """Normalize the contours."""
        # Calculate zonal statistics
        processing.run('qgis:zonalstatistics', {
            'INPUT_RASTER': elevation,
            'INPUT_VECTOR': contours,
            'RASTER_BAND': 1,
            'STATS' : [2], # mean
            'COLUMN_PREFIX' : '_'
        })

        contourInterval = self._getContourInterval()

        # Remove any polygons lower than the altitude interval
        it = contours.getFeatures(QgsFeatureRequest().setFilterExpression('_mean < %f' % contourInterval))
        contours.dataProvider().deleteFeatures([i.id() for i in it])

        # Add a virtual field containing the normalised height to the altitude interval
        field = QgsField('elevation', QVariant.Double)
        contours.addExpressionField('floor(_mean / %(interval)f) * %(interval)f' % {'interval': contourInterval}, field)
