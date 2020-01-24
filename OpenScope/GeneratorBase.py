"""The base class from which GIS generators should inherit"""
import os
import tempfile
from PyQt5.QtGui import QColor
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsMapLayer,
    QgsProject,
    QgsVectorLayer, QgsVectorFileWriter
)
from qgis.utils import iface
from .AirportModel import AirportModel

class GeneratorConfigBase:
    """The configuration options passed to the GeneratorBase constructor."""

    airportFile = None

    loadExistingTerrain = False

    projectPath = None

    terrainFile = None

    tmpPath = tempfile.gettempdir()

class GeneratorBase:
    """The base class from which GIS generators should inherit"""

    _airport = None

    _config = None

#------------------- Lifecycle -------------------

    def __init__(self, config):
        self._airport = AirportModel(config.airportFile)
        self._config = config

#------------------- Public -------------------

    def getAirport(self):
        """Gets the AirportModel."""
        return self._airport

    def getDemsPath(self):
        """Gets the location of where DEM files should be stored."""
        path = os.path.join(self.getTempPath(), 'dems')
        os.makedirs(path, exist_ok=True)
        return path

    def getGshhgPath(self):
        """Gets the location of where GSHHG files should be stored."""
        path = os.path.join(self.getTempPath(), 'gshhg')
        os.makedirs(path, exist_ok=True)
        return path

    def getIcao(self):
        """Gets the ICAO code of the airport."""
        return self.getAirport().getIcao()

    def getOgrString(self, name, fileName=None):
        """Gets the OGR string for the the specified name"""

        if not fileName:
            fileName = name

        fileName = os.path.join(self.getProjectPath(), '%s.gpkg' % fileName)

        return 'ogr:dbname=\'%s\' table="%s" (geom) sql=' % (fileName, name)

    def getProjectPath(self):
        """Gets the location of where project files for the airport should be stored."""
        path = os.path.join(self._config.projectPath, self.getIcao())
        os.makedirs(path, exist_ok=True)
        return path

    def getTempPath(self):
        """Gets the temporary directory."""
        return os.path.join(self._config.tmpPath, 'qgsopenscope')

    def addGroup(self, name, parent=None):
        """Add a group to the project's layer tree."""
        if not parent:
            parent = QgsProject.instance().layerTreeRoot()
        return parent.addGroup(name)

    def addLayerToGroup(self, layer, group):
        """Add the layer to the specified group."""
        QgsProject.instance().addMapLayer(layer, False)
        group.addLayer(layer)

    def createMemoryLayer(self, name, layerType, fields=None):
        """Creates a new in-memory QgsVectorLayer."""
        layer = QgsVectorLayer('%s?crs=epsg:4326' % layerType, name, 'memory')

        if fields is not None:
            layer.dataProvider().addAttributes(fields)
            layer.updateFields()

        return layer

    def createVectorLayer(self, name, layerType, fields=None, fileName=None):
        """Creates a new QgsVectorLayer."""
        if not fileName:
            fileName = name
        fileName = os.path.join(self.getProjectPath(), '%s.gpkg' % fileName)

        layer = self.createMemoryLayer(name, layerType, fields)

        QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            fileName,
            'utf-8',
            layer.crs(),
            'GPKG'
        )

        return QgsVectorLayer(fileName, name)

    def loadExistingTerrain(self, group):
        """Loads the existing terrrain, if present"""

        terrainFile = self._config.terrainFile

        # Make a guess of where the terrain file is located
        if not terrainFile or not os.path.isfile(terrainFile):
            terrainFile = os.path.join(
                os.path.dirname(self._config.airportFile),
                'terrain',
                '%s.geojson' % str.lower(self.getIcao())
            )

        if not os.path.isfile(terrainFile):
            return

        layer = QgsVectorLayer(terrainFile)
        layer.setName('Existing Terrain')
        layer.setReadOnly(True)

        # Styling
        if layer.renderer():
            layer.renderer().symbol().setColor(QColor.fromRgb(0xff, 0x9e, 0x17))

        # Load the layer, but don't display by default
        self.addLayerToGroup(layer, group)
        QgsProject.instance().layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(False)

    def saveProject(self):
        """Saves the project"""

        icao = self.getIcao()
        fileName = os.path.join(self.getProjectPath(), '%s.qgs' % icao)

        project = QgsProject.instance()
        metadata = project.metadata()

        metadata.addKeywords('icao', [icao])

        project.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
        project.setMetadata(metadata)

        if not project.fileName():
            project.setFileName(fileName)

        project.write()

    def zoomToGroup(self, group=None):
        """Zoom to the layers in the specified group"""
        canvas = iface.mapCanvas()
        bounds = None

        if not group:
            group = QgsProject.instance().layerTreeRoot()

        for item in group.findLayers():
            layer = item.layer()

            if layer.type() != QgsMapLayer.VectorLayer:
                continue

            extent = item.layer().extent()

            if not extent.isEmpty():
                if bounds is None:
                    bounds = extent
                else:
                    bounds.combineExtentWith(extent)

        if bounds is not None and not bounds.isEmpty():
            canvas.setExtent(bounds)

        canvas.refreshAllLayers()
