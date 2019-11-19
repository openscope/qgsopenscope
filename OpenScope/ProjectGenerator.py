"""The project generator."""
from enum import Enum, IntFlag
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from qgis.core import (
    QgsFeature, QgsField,
    QgsGeometry,
    QgsMarkerSymbol,
    QgsPalLayerSettings, QgsProject,
    QgsVectorLayerSimpleLabeling
)
from qgis.utils import iface
from .GeneratorBase import GeneratorBase, GeneratorConfigBase

_MEMORY_OUTPUT = 'memory:'

class LayerName(Enum):
    """A list of value names for layers or groups"""
    Airport = 'Airport'
    Airspace = 'Airspace'
    AirspaceHidden = 'Airspace (Hidden)'
    ExistingTerrain = 'Exiting Terrain'
    Fixes = 'Fixes'
    Maps = 'Maps'
    Restricted = 'Restricted'
    Terrain = 'Terrain'

class LayerType(IntFlag):
    """A list of valid values for type of layer to import"""
    Empty = 0x0
    All = 0x7fffffff
    Airspace = 0x1
    AirspaceHidden = 0x2
    ExistingTerrain = 0x20
    Fixes = 0x4
    Maps = 0x8
    Restricted = 0x10

class ProjectGeneratorConfig(GeneratorConfigBase):
    """The configuration options passed to the ProjectGenerator constructor."""

    layers = LayerType.Empty

    mapNames = []

class ProjectGenerator(GeneratorBase):
    """The project generator."""

#------------------- Public -------------------

    def populateProject(self, _feedback=None):
        """Populates the project."""

        root = QgsProject.instance().layerTreeRoot()
        layersToAdd = self._config.layers

        airportGroup = root.findGroup(LayerName.Airport.value) or self.addGroup(LayerName.Airport.value)
        mapsGroup = root.findGroup(LayerName.Maps.value) or self.addGroup(LayerName.Maps.value)
        terrainGroup = root.findGroup(LayerName.Terrain.value) or self.addGroup(LayerName.Terrain.value)
        airspaceGroup = root.findGroup(LayerName.Airspace.value) or self.addGroup(LayerName.Airspace.value)

        if LayerType.Fixes in layersToAdd:
            self._generateFixes(airportGroup)

        if LayerType.Restricted in layersToAdd:
            self._generateRestricted(airportGroup)

        if LayerType.Airspace in layersToAdd:
            self._generateAirspace(airspaceGroup)

        if LayerType.AirspaceHidden in layersToAdd:
            self._generateAirspace(airspaceGroup, True)

        if LayerType.Maps in layersToAdd:
            self._generateMaps(mapsGroup)

        if LayerType.ExistingTerrain in layersToAdd:
            self.loadExistingTerrain(terrainGroup)

        iface.setActiveLayer(root.findLayer(LayerName.Airspace.value))

        self.zoomToAllLayers()

    @staticmethod
    def hasExistingLayers(layerType=LayerType.All):
        """Gets a flag indicating whether the project has existing layers or groups"""

        project = QgsProject.instance()
        root = project.layerTreeRoot()

        if layerType == LayerType.All:
            return root.children() != []

        if LayerType.Airspace in layerType:
            if project.mapLayersByName(LayerName.Airspace.value):
                return True

        if LayerType.AirspaceHidden in layerType:
            if project.mapLayersByName(LayerName.AirspaceHidden.value):
                return True

        if LayerType.Fixes in layerType:
            if project.mapLayersByName(LayerName.Fixes.value):
                return True

        if LayerType.Maps in layerType:
            mapGroup = root.findGroup(LayerName.Maps.value)
            if mapGroup and mapGroup.children():
                return True

        if LayerType.Restricted in layerType:
            if project.mapLayersByName(LayerName.Restricted.value):
                return True

        return False

#------------------- Private -------------------

    def _addAirspaceLayer(self, group, layerName):
        """Adds the airspace layer to the project"""

        fields = [
            QgsField('name', QVariant.String),
            QgsField('airspace_class', QVariant.String),
            QgsField('floor', QVariant.Int),
            QgsField('ceiling', QVariant.Int)
        ]
        layer = self.createVectorLayer(layerName, 'Polygon', fields)

        # Colour
        layer.renderer().symbol().setColor(QColor.fromRgb(0x00, 0xff, 0x00))

        # Labeling
        settings = QgsPalLayerSettings()
        settings.fieldName = """coalesce(\"name\", 'No Name') || ' - ' ||
        'FL' || \"floor\" || ' to ' || 'FL' || \"ceiling\" ||
        ' (Class ' || \"airspace_class\" || ')'"""
        settings.isExpression = True
        settings.placement = QgsPalLayerSettings.PerimeterCurved
        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        layer.setLabelsEnabled(True)
        layer.triggerRepaint()

        self.addLayerToGroup(layer, group)

        return layer

    def _addFixesLayer(self, group, layerName):
        """Adds the fixes layer to the project"""

        fields = [
            QgsField('name', QVariant.String),
        ]
        layer = self.createVectorLayer(layerName, 'Point', fields)

        # Symbol
        symbol = QgsMarkerSymbol.createSimple({
            'name': 'equilateral_triangle',
            'color': 'white',
            'stroke': 'black',
            'size': '3'
        })
        layer.renderer().setSymbol(symbol)

        # Labeling
        settings = QgsPalLayerSettings()
        settings.fieldName = '"name"'
        settings.isExpression = True
        settings.placement = QgsPalLayerSettings.OverPoint
        settings.quadOffset = QgsPalLayerSettings.QuadrantAboveRight
        settings.distance = '1'
        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        layer.setLabelsEnabled(True)
        layer.triggerRepaint()

        self.addLayerToGroup(layer, group)

        return layer

    def _addMapLayer(self, group, mapName):
        """Adds the Map layer to the project"""

        layer = self.createVectorLayer(mapName, 'LineString', fileName='Map - %s' % mapName)

        sym = layer.renderer().symbol()
        sym.setColor(QColor.fromRgb(0x00, 0x00, 0x00))
        sym.setWidth(0.33)

        self.addLayerToGroup(layer, group)

        return layer

    def _addRestrictedLayer(self, group, layerName):
        """Adds the Restricted airspaces to the project"""

        fields = [
            QgsField('name', QVariant.String),
            QgsField('height', QVariant.String),
        ]
        layer = self.createVectorLayer(layerName, 'Polygon', fields)

        # Colour
        layer.renderer().symbol().setColor(QColor.fromRgb(0xff, 0x60, 0x60))

        # Labeling
        settings = QgsPalLayerSettings()
        settings.fieldName = '"name" || \'\\n0ft\\n\' || "height"'
        settings.isExpression = True
        settings.placement = QgsPalLayerSettings.AroundPoint
        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        layer.setLabelsEnabled(True)
        layer.triggerRepaint()

        self.addLayerToGroup(layer, group)

        return layer

    def _generateAirspace(self, group, hiddenAirspace=False):
        """Generate the Airspace layer."""

        layerName = LayerName.AirspaceHidden.value if hiddenAirspace else LayerName.Airspace.value
        found = QgsProject.instance().mapLayersByName(layerName)
        layer = None
        features = []

        if found:
            layer = found[0]
            layer.dataProvider().truncate()
        else:
            layer = self._addAirspaceLayer(group, layerName)

        for a in self.getAirport().getAirspace(hiddenAirspace):
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPolygonXY([a.poly]))
            feature.setAttributes([
                None, # ID
                a.name,
                a.airspaceClass,
                a.floor,
                a.ceiling
            ])
            features.append(feature)

        layer.dataProvider().addFeatures(features)

        return layer

    def _generateFixes(self, group):
        """Generate the Fixes layer."""

        layerName = LayerName.Fixes.value
        found = QgsProject.instance().mapLayersByName(layerName)
        layer = None
        features = []

        if found:
            layer = found[0]
            layer.dataProvider().truncate()
        else:
            layer = self._addFixesLayer(group, layerName)

        for p in self.getAirport().getFixes():
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPointXY(p.location))
            feature.setAttributes([
                None,
                p.name
            ])
            features.append(feature)

        layer.dataProvider().addFeatures(features)

    def _generateMaps(self, group):
        """Generates the Map layers."""

        mapNames = self._config.mapNames

        for m in self.getAirport().getMaps():
            name = m.name

            if name not in mapNames:
                continue

            found = QgsProject.instance().mapLayersByName(name)
            layer = None
            features = []

            if found:
                layer = found[0]
                layer.dataProvider().truncate()
            else:
                layer = self._addMapLayer(group, name)

            for l in m.lines:
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolylineXY(l))
                features.append(feature)

            layer.dataProvider().addFeatures(features)

    def _generateRestricted(self, group):
        """Generate the Restricted layer."""

        layerName = LayerName.Restricted.value
        found = QgsProject.instance().mapLayersByName(layerName)
        layer = None
        features = []

        if found:
            layer = found[0]
            layer.dataProvider().truncate()
        else:
            layer = self._addRestrictedLayer(group, layerName)

        for r in self.getAirport().getRestricted():
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPolygonXY([r.coordinates]))
            feature.setAttributes([
                None, # ID
                r.name,
                r.height
            ])
            features.append(feature)

        layer.dataProvider().addFeatures(features)

        return layer
