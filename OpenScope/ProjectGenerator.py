"""The project generator."""
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

class ProjectGeneratorConfig(GeneratorConfigBase):
    """The configuration options passed to the ProjectGenerator constructor."""

class ProjectGenerator(GeneratorBase):
    """The project generator."""

#------------------- Public -------------------

    def populateProject(self, _feedback=None):
        """Populates the project."""
        QgsProject.instance().clear()

        root = QgsProject.instance().layerTreeRoot()

        self._generateFixes(root)
        self._generateRestricted(root)

        maps = self.addGroup('Maps')
        terrain = self.addGroup('Terrain')

        airspace = self._generateAirspace(root)
        self._generateAirspace(root, True)
        self._generateMaps(maps)

        if self._config.loadExistingTerrain:
            self.loadExistingTerrain(terrain)

        iface.setActiveLayer(airspace)

        self.zoomToAllLayers()

    @staticmethod
    def hasExistingLayers():
        """Gets a flag indicating whether the project has existing layers or groups"""
        return QgsProject.instance().layerTreeRoot().children() != []

#------------------- Private -------------------

    def _generateAirspace(self, group, hiddenAirspace=False):
        """Generate the Airspace layer."""
        fields = [
            QgsField('name', QVariant.String),
            QgsField('airspace_class', QVariant.String),
            QgsField('floor', QVariant.Int),
            QgsField('ceiling', QVariant.Int)
        ]
        layerName = 'Airspace (Hidden)' if hiddenAirspace else 'Airspace'
        layer = self.createVectorLayer(layerName, 'Polygon', fields)
        features = []

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

    def _generateFixes(self, group):
        """Generate the Fixes layer."""
        fields = [
            QgsField('name', QVariant.String),
        ]
        layer = self.createVectorLayer('Fixes', 'Point', fields)
        features = []

        for p in self.getAirport().getFixes():
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPointXY(p.location))
            feature.setAttributes([
                None,
                p.name
            ])
            features.append(feature)

        layer.dataProvider().addFeatures(features)

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

    def _generateMaps(self, group):
        """Generates the Map layers."""
        for m in self.getAirport().getMaps():
            layer = self.createVectorLayer(m.name, 'LineString', fileName='Map - %s' % m.name)
            features = []

            for l in m.lines:
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolylineXY(l))
                features.append(feature)

            layer.dataProvider().addFeatures(features)

            sym = layer.renderer().symbol()
            sym.setColor(QColor.fromRgb(0x00, 0x00, 0x00))
            sym.setWidth(0.33)

            self.addLayerToGroup(layer, group)

    def _generateRestricted(self, group):
        """Generate the Restricted layer."""
        fields = [
            QgsField('name', QVariant.String),
            QgsField('height', QVariant.String),
        ]
        layer = self.createVectorLayer('Restricted', 'Polygon', fields)
        features = []

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
