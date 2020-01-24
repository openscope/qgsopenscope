"""The terrain generator."""
import os
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from qgis.core import (
    QgsFeature, QgsFeatureRequest, QgsField,
    QgsGeometry,
    QgsMapLayer,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsWkbTypes
)
import processing # pylint: disable=import-error
from .GeneratorBase import GeneratorBase, GeneratorConfigBase
from .utilities.dem import getDemFromLayer
from .utilities.gshhg import (
    downloadArchive,
    getRiverShapeFile,
    getShorelineShapeFile,
    Resolution,
    RiverLevel,
    ShorelineLevel
)

_MEMORY_OUTPUT = 'memory:'

_WDB_RIVER_LEVELS = [
    RiverLevel.DOUBLE_LINED_RIVER,
    RiverLevel.PERMAMENT_MAJOR_RIVER,
    RiverLevel.ADDITIONAL_MAJOR_RIVER
]

class TerrainGeneratorConfig(GeneratorConfigBase):
    """The configuration options passed to the TerrainGenerator constructor."""

    contourInterval = 304.8

class TerrainGenerator(GeneratorBase):
    """The terrain generator."""

#------------------- Public -------------------

    def generateTerrain(self, feedback):
        """Generates the terrain"""

        project = QgsProject.instance()
        terrain = TerrainGenerator._getTerrainGroup()

        if terrain:
            layers = list(map(lambda x: x.layer().id(), terrain.findLayers()))
            project.removeMapLayers(layers)
        else:
            terrain = self.addGroup('Terrain')

        polygons = self._getSelectedPolygons()

        if not polygons:
            raise Exception('No valid polygons were selected to determine the terrain bounds')

        if self._config.loadExistingTerrain:
            self.loadExistingTerrain(terrain)

        # Ensure the GSHHG data is present
        feedback.setProgressText('Downloading GSHHG archive')
        feedback.setProgress(0)
        downloadArchive(self.getGshhgPath(), feedback)

        # Get the clipping bounds
        bounds, perimeter, buffer = self._getPerimeter(polygons, feedback)
        # self.addLayerToGroup(airspace, group)
        # self.addLayerToGroup(perimeter, group)
        # self.addLayerToGroup(buffer, group)

        self._generateRivers(terrain, buffer, feedback)

        self._generateTerrain(terrain, bounds, perimeter, buffer, feedback)

        # Clean up unused layers
        project.removeMapLayers([
            bounds.id(),
            perimeter.id(),
            buffer.id()
        ])

        self.zoomToGroup(terrain)

    @staticmethod
    def hasExistingLayers():
        """Gets a flag indicating whether there are existing terrain layers"""
        group = TerrainGenerator._getTerrainGroup()
        return group is not None and group.findLayers() != []

#------------------- Private -------------------

    def _generateRivers(self, terrain, buffer, feedback):
        """Generates the river lines within the buffer"""

        rivers = self.createVectorLayer('Rivers', 'LineString', fileName='Rivers')
        features = []

        self._setProgress(feedback, 'Clipping and simplifying rivers')
        for level in _WDB_RIVER_LEVELS:
            shpPath = getRiverShapeFile(self.getGshhgPath(), Resolution.FULL, level)

            result = processing.run('qgis:clip', {
                'INPUT': shpPath,
                'OUTPUT': _MEMORY_OUTPUT,
                'OVERLAY': buffer
            }, feedback=feedback)

            result = processing.run('qgis:simplifygeometries', {
                'INPUT': result['OUTPUT'],
                'METHOD': 0, # Distance
                'OUTPUT': _MEMORY_OUTPUT,
                'TOLERANCE': 0.0005
            }, feedback=feedback)

            for f in result['OUTPUT'].getFeatures():
                newFeature = QgsFeature()

                newFeature.setGeometry(f.geometry())
                features.append(newFeature)

        rivers.dataProvider().addFeatures(features)

        sym = rivers.renderer().symbol()
        sym.setColor(QColor.fromRgb(0x00, 0xff, 0xff))
        sym.setWidth(0.66)

        self.addLayerToGroup(rivers, terrain)

    def _generateTerrain(self, group, bounds, perimeter, buffer, feedback):
        """Generate the terrain."""

        # Get the water
        self._setProgress(feedback, 'Getting water')
        water = self._getWater(bounds, buffer, feedback)
        self.addLayerToGroup(water, group)

        # Height data
        mergedDem, clippedDem, contours = self._getElevationData(buffer, feedback)
        # self.addLayerToGroup(mergedDem, group)
        # self.addLayerToGroup(clippedDem, group)
        # self.addLayerToGroup(contours, group)

        # Clean the contours
        cleaned = self._getCleanContours(contours, perimeter, bounds, feedback)
        self.addLayerToGroup(cleaned, group)

        # Normalize the contours
        self._normalizeContours(cleaned, clippedDem, feedback)

        # Clean up unused layers
        QgsProject.instance().removeMapLayers([
            mergedDem.id(),
            clippedDem.id(),
            contours.id()
        ])

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

    def _getCleanContours(self, contours, perimeter, airspace, feedback):
        """Get the cleaned contours."""
        # Simplify the contours
        self._setProgress(feedback, 'Simplify contours')
        result = processing.run('qgis:simplifygeometries', {
            'INPUT': contours,
            'TOLERANCE': 0.002,
            'OUTPUT': _MEMORY_OUTPUT
        }, feedback=feedback)
        simplified = result['OUTPUT']
        simplified.setName('Contours - Simplified')

        # Merge with perimeter
        self._setProgress(feedback, 'Merging contours with perimter')
        result = processing.run('qgis:mergevectorlayers', {
            'LAYERS': [simplified, perimeter],
            'OUTPUT': _MEMORY_OUTPUT
        }, feedback=feedback)
        merged = result['OUTPUT']
        merged.setName('Contours - Merged')

        # Polygonise
        self._setProgress(feedback, 'Polygonise contours')
        result = processing.run('qgis:polygonize', {
            'INPUT': merged,
            'OUTPUT': _MEMORY_OUTPUT,
        })
        polygons = result['OUTPUT']
        polygons.setName('Contours - Polygons')

        # Select all polygons smaller than 0.0005 sq degrees (about 38ha at lat=52))
        # and eliminate them
        self._setProgress(feedback, 'Eliminating small contour polygons')
        selection = polygons.getFeatures(QgsFeatureRequest().setFilterExpression('$area < 0.00005'))
        polygons.selectByIds([k.id() for k in selection])

        result = processing.run('qgis:eliminateselectedpolygons', {
            'INPUT': polygons,
            'OUTPUT': _MEMORY_OUTPUT,
            'MODE': 2 # Largest common boundary
        }, feedback=feedback)
        cleaned = result['OUTPUT']
        cleaned.setName('Contours - Cleaned')

        # Delete any features that weren't eliminated (outside a common boundary)
        self._setProgress(feedback, 'Deleting remaining small contour polygons')
        selection = cleaned.getFeatures(QgsFeatureRequest().setFilterExpression('$area < 0.00005'))
        cleaned.dataProvider().deleteFeatures([k.id() for k in selection])

        # Clip to airspace
        self._setProgress(feedback, 'Clipping contours to bounds')
        result = processing.run('qgis:clip', {
            'INPUT': cleaned,
            'OUTPUT': _MEMORY_OUTPUT,
            'OVERLAY': airspace
        })
        clipped = result['OUTPUT']
        clipped.setName('Contours - Clipped')

        # Multipart to single part
        self._setProgress(feedback, 'Converting contours to single part')
        result = processing.run('qgis:multiparttosingleparts', {
            'INPUT': clipped,
            'OUTPUT': self.getOgrString('Contours - Final')
        }, feedback=feedback)
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
        self._setProgress(feedback, 'Getting DEM files')
        demFiles = getDemFromLayer(self.getDemsPath(), boundingLayer, feedback)

        projectPath = self.getProjectPath()

        # Merge all the DEM files into a single geotiff
        self._setProgress(feedback, 'Merging DEM files')
        mergedFile = os.path.join(projectPath, 'Elevation - Merged.tif')
        if os.path.isfile(mergedFile):
            os.unlink(mergedFile)

        result = processing.run('gdal:merge', {
            'INPUT': demFiles,
            'DATA_TYPE': 1,
            'OUTPUT': mergedFile
        }, feedback=feedback)
        merged = QgsRasterLayer(result['OUTPUT'], 'Elevation - Merged')

        # Clip the DEM file to the bounds
        self._setProgress(feedback, 'Clipping merged DEM')
        clippedFile = os.path.join(projectPath, 'Elevation - Clipped.tif')
        if os.path.isfile(clippedFile):
            os.unlink(clippedFile)

        result = processing.run('gdal:cliprasterbymasklayer', {
            'INPUT': mergedFile,
            'MASK': boundingLayer,
            'OUTPUT': clippedFile
        }, feedback=feedback)
        clipped = QgsRasterLayer(result['OUTPUT'], 'Elevation - Clipped')

        # Generate the contours
        self._setProgress(feedback, 'Generating contours')
        contourFile = os.path.join(projectPath, 'Contours.shp')
        if os.path.isfile(contourFile):
            os.unlink(contourFile)

        result = processing.run('gdal:contour', {
            'INPUT': clippedFile,
            'BAND' : 1,
            'INTERVAL': self._getContourInterval(),
            'OUTPUT': contourFile
        }, feedback=feedback)
        contours = QgsVectorLayer(result['OUTPUT'], 'Contours')

        # Remove any polygons at or below sea level
        self._setProgress(feedback, 'Removing contours at or below sea level')
        it = contours.getFeatures(QgsFeatureRequest().setFilterExpression('ELEV <= %f' % 0))
        contours.dataProvider().deleteFeatures([i.id() for i in it])

        return (merged, clipped, contours)

    def _getPerimeter(self, polygons, feedback):
        """Gets the perimeter for the terrain"""

        bounds = self._getBounds(polygons)

        # Perimeter
        self._setProgress(feedback, 'Getting perimiter')
        result = processing.run('qgis:polygonstolines', {
            'INPUT': bounds,
            'OUTPUT': _MEMORY_OUTPUT
        }, feedback=feedback)
        perimeter = result['OUTPUT']
        perimeter.setName('Perimeter')

        # Buffer the airspace
        self._setProgress(feedback, 'Buffering perimiter')
        result = processing.run('qgis:buffer', {
            'INPUT': bounds,
            'OUTPUT': _MEMORY_OUTPUT,
            'DISTANCE': 0.05
        }, feedback=feedback)
        buffer = result['OUTPUT']
        buffer.setName('Buffer')

        return (bounds, perimeter, buffer)

    def _getSelectedPolygons(self):
        """Gets the list of selected polygons"""

        selected = []

        for layerView in QgsProject.instance().layerTreeRoot().findLayers():
            layer = layerView.layer()

            if layer.type() != QgsMapLayer.VectorLayer:
                continue

            features = filter(
                lambda x: x.geometry().type() == QgsWkbTypes.PolygonGeometry,
                layer.selectedFeatures()
            )

            selected.extend(features)

        return selected

    @staticmethod
    def _getTerrainGroup():
        """Gets the terrain group"""
        return QgsProject.instance().layerTreeRoot().findGroup('Terrain')

    def _getWater(self, airspace, buffer, feedback):
        """Get the water layer."""
        gshhsPath = self.getGshhgPath()

        self._setProgress(feedback, 'Loading coastlines and lakes')
        coastlinePath = getShorelineShapeFile(gshhsPath, Resolution.FULL, ShorelineLevel.CONTINENTAL)
        coastlines = QgsVectorLayer(coastlinePath, 'Coastline')
        lakesPath = getShorelineShapeFile(gshhsPath, Resolution.FULL, ShorelineLevel.LAKES)
        lakes = QgsVectorLayer(lakesPath, 'Lakes')

        # Clip by the buffer
        self._setProgress(feedback, 'Clipping coastlines to buffer')
        result = processing.run('qgis:clip', {
            'INPUT': coastlines,
            'OVERLAY': buffer,
            'OUTPUT': _MEMORY_OUTPUT
        }, feedback=feedback)
        clipped_coastlines = result['OUTPUT']

        result = processing.run('qgis:clip', {
            'INPUT': lakes,
            'OVERLAY': buffer,
            'OUTPUT': _MEMORY_OUTPUT
        }, feedback=feedback)
        clipped_lakes = result['OUTPUT']

        # Simplify
        self._setProgress(feedback, 'Simplify coastline geometries')
        result = processing.run('qgis:simplifygeometries', {
            'INPUT': clipped_coastlines,
            'TOLERANCE': 0.002,
            'OUTPUT': _MEMORY_OUTPUT
        }, feedback=feedback)
        cleaned = result['OUTPUT']

        # Delete any small islands
        self._setProgress(feedback, 'Deleting small islands')
        it = cleaned.getFeatures(QgsFeatureRequest().setFilterExpression('$area < 0.0005'))
        cleaned.dataProvider().deleteFeatures([i.id() for i in it])

        # Invert to get the water
        self._setProgress(feedback, 'Inverting coastline')
        result = processing.run('qgis:difference', {
            'INPUT': buffer,
            'OVERLAY': cleaned,
            'OUTPUT': _MEMORY_OUTPUT
        }, feedback=feedback)
        difference = result['OUTPUT']

        # Merge sea with lakes
        self._setProgress(feedback, 'Combining lakes and sea')
        result = processing.run('qgis:mergevectorlayers', {
            'LAYERS': [difference, clipped_lakes],
            'OUTPUT': _MEMORY_OUTPUT
        }, feedback=feedback)
        merged_water = result['OUTPUT']

        # Re-clip by the airspace
        self._setProgress(feedback, 'Clipping water to airspace')
        result = processing.run('qgis:clip', {
            'INPUT': merged_water,
            'OVERLAY': airspace,
            'OUTPUT': _MEMORY_OUTPUT
        })
        clipped = result['OUTPUT']

        # Multipart to single part
        self._setProgress(feedback, 'Converting water to single part')
        result = processing.run('qgis:multiparttosingleparts', {
            'INPUT': clipped,
            'OUTPUT': self.getOgrString('Water')
        }, feedback=feedback)
        water = result['OUTPUT']
        water.setName('Water')

        # Delete any small area of water
        self._setProgress(feedback, 'Deleting small areas of water')
        it = water.getFeatures(QgsFeatureRequest().setFilterExpression('$area < 0.0005'))
        water.dataProvider().deleteFeatures([i.id() for i in it])

        # Add an elevation attribute (0)
        self._setProgress(feedback, 'Adding height data')
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

    def _normalizeContours(self, contours, elevation, feedback):
        """Normalize the contours."""
        # Calculate zonal statistics
        self._setProgress(feedback, 'Calculating zonal statistics')
        processing.run('qgis:zonalstatistics', {
            'INPUT_RASTER': elevation,
            'INPUT_VECTOR': contours,
            'RASTER_BAND': 1,
            'STATS' : [2], # mean
            'COLUMN_PREFIX' : '_'
        }, feedback=feedback)

        contourInterval = self._getContourInterval()

        # Remove any polygons lower than the altitude interval
        self._setProgress(feedback, 'Removing contours below min interval')
        it = contours.getFeatures(QgsFeatureRequest().setFilterExpression('_mean < %f' % contourInterval))
        contours.dataProvider().deleteFeatures([i.id() for i in it])

        # Add a virtual field containing the normalised height to the altitude interval
        field = QgsField('elevation', QVariant.Double)
        contours.addExpressionField('floor(_mean / %(interval)f) * %(interval)f' % {'interval': contourInterval}, field)

    def _setProgress(self, feedback, text):
        """Updates the progress for the feedback object"""
        feedback.setProgressText(text)
        feedback.setProgress(0)
