"""The base class from which GIS generators should inherit"""
import os
import tempfile
from qgis.core import (
    QgsProject,
    QgsRectangle,
    QgsVectorLayer, QgsVectorFileWriter
)
from qgis.utils import iface

class GeneratorConfigBase:
    """The configuration options passed to the GeneratorBase constructor."""

    tmpPath = tempfile.gettempdir()

class GeneratorBase:
    """The base class from which GIS generators should inherit"""

    _airport = None

    _config = None

#------------------- Lifecycle -------------------

    def __init__(self, airport, config):
        self._airport = airport
        self._config = config

#------------------- Public -------------------

    def getAirport(self):
        """Gets the AirportModel."""
        return self._airport

    def getAirportPath(self):
        """Gets the location of where temporary files for the airport should be stored."""
        path = os.path.join(self.getTempPath(), self.getIcao())
        os.makedirs(path, exist_ok=True)
        return path

    def getDemsPath(self):
        """Gets the location of where DEM files should be stored."""
        path = os.path.join(self.getTempPath(), 'dems')
        os.makedirs(path, exist_ok=True)
        return path

    def getIcao(self):
        """Gets the ICAO code of the airport."""
        return self.getAirport().getIcao()

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
        fileName = os.path.join(self.getAirportPath(), '%s.gpkg' % fileName)

        layer = self.createMemoryLayer(name, layerType, fields)

        QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            fileName,
            'utf-8',
            layer.crs(),
            'GPKG'
        )

        return QgsVectorLayer(fileName, name)

    def zoomToAllLayers(self):
        """Zoom to the buffered area and redraw"""
        canvas = iface.mapCanvas()
        bounds = QgsRectangle()

        for item in QgsProject.instance().layerTreeRoot().findLayers():
            extent = item.layer().extent()

            if not extent.isEmpty():
                bounds.combineExtentWith(extent)

        canvas.setExtent(bounds)
        canvas.refreshAllLayers()
