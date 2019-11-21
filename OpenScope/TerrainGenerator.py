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

_MEMORY_OUTPUT = 'memory:'
_WDB_RES = 'f'
_WDB_RIVER_LEVELS = [1, 2, 3]

class TerrainGeneratorConfig(GeneratorConfigBase):
    """The configuration options passed to the TerrainGenerator constructor."""

    contourInterval = 304.8

    gshhsPath = None

class TerrainGenerator(GeneratorBase):
    """The terrain generator."""

#------------------- Public -------------------

    def generateTerrain(self, feedback=None):
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

        # Get the clipping bounds
        bounds, perimeter, buffer = self._getPerimeter(polygons)
        # self.addLayerToGroup(airspace, group)
        # self.addLayerToGroup(perimeter, group)
        # self.addLayerToGroup(buffer, group)

        self._generateRivers(terrain, buffer)

        self._generateTerrain(terrain, bounds, perimeter, buffer, feedback)

        # Clean up unused layers
        project.removeMapLayers([
            bounds.id(),
            perimeter.id(),
            buffer.id()
        ])

    @staticmethod
    def hasExistingLayers():
        """Gets a flag indicating whether there are existing terrain layers"""
        group = TerrainGenerator._getTerrainGroup()
        return group is not None and group.findLayers() != []

#------------------- Private -------------------

    def _generateRivers(self, terrain, buffer):
        """Generates the river lines within the buffer"""

        wdbPath = os.path.join(self._config.gshhsPath, 'WDBII_shp', _WDB_RES)
        rivers = self.createVectorLayer('Rivers', 'LineString', fileName='Rivers')
        features = []

        print('Clipping and simplifying rivers')
        for level in _WDB_RIVER_LEVELS:
            levelName = 'WDBII_river_%s_L%02d' % (_WDB_RES, level)
            shpPath = os.path.join(wdbPath, '%s.shp' % levelName)

            result = processing.run('qgis:clip', {
                'INPUT': shpPath,
                'OUTPUT': _MEMORY_OUTPUT,
                'OVERLAY': buffer
            })

            result = processing.run('qgis:simplifygeometries', {
                'INPUT': result['OUTPUT'],
                'METHOD': 0, # Distance
                'OUTPUT': _MEMORY_OUTPUT,
                'TOLERANCE': 0.0005
            })

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
        print("Getting water")
        water = self._getWater(bounds, buffer)
        self.addLayerToGroup(water, group)

        # Height data
        mergedDem, clippedDem, contours = self._getElevationData(buffer, feedback)
        # self.addLayerToGroup(mergedDem, group)
        # self.addLayerToGroup(clippedDem, group)
        # self.addLayerToGroup(contours, group)

        # Clean the contours
        cleaned = self._getCleanContours(contours, perimeter, bounds)
        self.addLayerToGroup(cleaned, group)

        # Normalize the contours
        self._normalizeContours(cleaned, clippedDem)

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

    def _getCleanContours(self, contours, perimeter, airspace):
        """Get the cleaned contours."""
        # Simplify the contours
        print("Simplify contours")
        result = processing.run('qgis:simplifygeometries', {
            'INPUT': contours,
            'TOLERANCE': 0.002,
            'OUTPUT': _MEMORY_OUTPUT
        })
        simplified = result['OUTPUT']
        simplified.setName('Contours - Simplified')

        # Merge with perimeter
        print("Merging contours with perimter")
        result = processing.run('qgis:mergevectorlayers', {
            'LAYERS': [simplified, perimeter],
            'OUTPUT': _MEMORY_OUTPUT
        })
        merged = result['OUTPUT']
        merged.setName('Contours - Merged')

        # Polygonise
        print("Polygonise contours")
        result = processing.run('qgis:polygonize', {
            'INPUT': merged,
            'OUTPUT': _MEMORY_OUTPUT,
        })
        polygons = result['OUTPUT']
        polygons.setName('Contours - Polygons')

        # Select all polygons smaller than 0.0005 sq degrees (about 38ha at lat=52))
        # and eliminate them
        print("Eliminating small contour polygons")
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
        print("Deleting remaining small contour polygons")
        selection = cleaned.getFeatures(QgsFeatureRequest().setFilterExpression('$area < 0.00005'))
        cleaned.dataProvider().deleteFeatures([k.id() for k in selection])

        # Clip to airspace
        print("Clipping contours to bounds")
        result = processing.run('qgis:clip', {
            'INPUT': cleaned,
            'OUTPUT': _MEMORY_OUTPUT,
            'OVERLAY': airspace
        })
        clipped = result['OUTPUT']
        clipped.setName('Contours - Clipped')

        # Multipart to single part
        print("Converting contours to single part")
        result = processing.run('qgis:multiparttosingleparts', {
            'INPUT': clipped,
            'OUTPUT': self.getOgrString('Contours - Final')
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
        print("Getting DEM files")
        demFiles = getDemFromLayer(self.getDemsPath(), boundingLayer)

        projectPath = self.getProjectPath()

        # Merge all the DEM files into a single geotiff
        print("Merging DEM files")
        mergedFile = os.path.join(projectPath, 'Elevation - Merged.tif')
        if os.path.isfile(mergedFile):
            os.unlink(mergedFile)

        result = processing.run('gdal:merge', {
            'INPUT': demFiles,
            'DATA_TYPE': 1,
            'OUTPUT': mergedFile
        }, feedback)
        merged = QgsRasterLayer(result['OUTPUT'], 'Elevation - Merged')

        # Clip the DEM file to the bounds
        print("Clipping merged DEM")
        clippedFile = os.path.join(projectPath, 'Elevation - Clipped.tif')
        if os.path.isfile(clippedFile):
            os.unlink(clippedFile)

        result = processing.run('gdal:cliprasterbymasklayer', {
            'INPUT': mergedFile,
            'MASK': boundingLayer,
            'OUTPUT': clippedFile
        }, feedback)
        clipped = QgsRasterLayer(result['OUTPUT'], 'Elevation - Clipped')

        # Generate the contours
        print("Generating contours")
        contourFile = os.path.join(projectPath, 'Contours.shp')
        if os.path.isfile(contourFile):
            os.unlink(contourFile)

        result = processing.run('gdal:contour', {
            'INPUT': clippedFile,
            'BAND' : 1,
            'INTERVAL': self._getContourInterval(),
            'OUTPUT': contourFile
        })
        contours = QgsVectorLayer(result['OUTPUT'], 'Contours')

        # Remove any polygons at or below sea level
        print("Removing contours at or below sea level")
        it = contours.getFeatures(QgsFeatureRequest().setFilterExpression('ELEV <= %f' % 0))
        contours.dataProvider().deleteFeatures([i.id() for i in it])

        return (merged, clipped, contours)

    def _getPerimeter(self, polygons):
        """Gets the perimeter for the terrain"""

        bounds = self._getBounds(polygons)

        # Perimeter
        print("Getting perimiter")
        result = processing.run('qgis:polygonstolines', {
            'INPUT': bounds,
            'OUTPUT': _MEMORY_OUTPUT
        })
        perimeter = result['OUTPUT']
        perimeter.setName('Perimeter')

        # Buffer the airspace
        print("Buffering perimiter")
        result = processing.run('qgis:buffer', {
            'INPUT': bounds,
            'OUTPUT': _MEMORY_OUTPUT,
            'DISTANCE': 0.05
        })
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

    def _getWater(self, airspace, buffer):
        """Get the water layer."""
        gshhsPath = self._config.gshhsPath

        print("Loading coastlines and lakes")
        coastlines = QgsVectorLayer(os.path.join(gshhsPath, 'GSHHS_shp/f/GSHHS_f_L1.shp'), 'Coastline')
        lakes = QgsVectorLayer(os.path.join(gshhsPath, 'GSHHS_shp/f/GSHHS_f_L2.shp'), 'Lakes')

        # Clip by the buffer
        print("Clipping coastlines to buffer")
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
        print("Simplify coastline geometries")
        result = processing.run('qgis:simplifygeometries', {
            'INPUT': clipped_coastlines,
            'TOLERANCE': 0.002,
            'OUTPUT': _MEMORY_OUTPUT
        })
        cleaned = result['OUTPUT']

        # Delete any small islands
        print("Deleting small islands")
        it = cleaned.getFeatures(QgsFeatureRequest().setFilterExpression("$area < 0.0005"))
        cleaned.dataProvider().deleteFeatures([i.id() for i in it])

        # Invert to get the water
        print("Inverting coastline")
        result = processing.run('qgis:difference', {
            'INPUT': buffer,
            'OVERLAY': cleaned,
            'OUTPUT': _MEMORY_OUTPUT
        })
        difference = result['OUTPUT']

        # Merge sea with lakes
        print("Combining lakes and sea")
        result = processing.run('qgis:mergevectorlayers', {
            'LAYERS': [difference, clipped_lakes],
            'OUTPUT': _MEMORY_OUTPUT
        })
        merged_water = result['OUTPUT']

        # Re-clip by the airspace
        print("Clipping water to airspace")
        result = processing.run('qgis:clip', {
            'INPUT': merged_water,
            'OVERLAY': airspace,
            'OUTPUT': _MEMORY_OUTPUT
        })
        clipped = result['OUTPUT']

        # Multipart to single part
        print("Converting water to single part")
        result = processing.run('qgis:multiparttosingleparts', {
            'INPUT': clipped,
            'OUTPUT': self.getOgrString('Water')
        })
        water = result['OUTPUT']
        water.setName('Water')

        # Delete any small area of water
        print("Deleting small areas of water")
        it = water.getFeatures(QgsFeatureRequest().setFilterExpression("$area < 0.0005"))
        water.dataProvider().deleteFeatures([i.id() for i in it])

        # Add an elevation attribute (0)
        print("Adding height data")
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
        print("Calculating zonal statistics")
        processing.run('qgis:zonalstatistics', {
            'INPUT_RASTER': elevation,
            'INPUT_VECTOR': contours,
            'RASTER_BAND': 1,
            'STATS' : [2], # mean
            'COLUMN_PREFIX' : '_'
        })

        contourInterval = self._getContourInterval()

        # Remove any polygons lower than the altitude interval
        print("Removing contours below min interval")
        it = contours.getFeatures(QgsFeatureRequest().setFilterExpression('_mean < %f' % contourInterval))
        contours.dataProvider().deleteFeatures([i.id() for i in it])

        # Add a virtual field containing the normalised height to the altitude interval
        field = QgsField('elevation', QVariant.Double)
        contours.addExpressionField('floor(_mean / %(interval)f) * %(interval)f' % {'interval': contourInterval}, field)
