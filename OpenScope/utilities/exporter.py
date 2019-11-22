"""A collection of functions to help exporting data"""
from qgis.PyQt.QtWidgets import QApplication, QFileDialog, QMessageBox
from qgis.core import QgsProject, QgsVectorFileWriter
import processing # pylint: disable=import-error
from .converters import EXPORT_PRECISION
from ..AirspaceModel import AirspaceModel
from ..FixModel import FixModel
from ..MapModel import MapModel
from ..RestrictedModel import RestrictedModel

#------------------- Public -------------------

def exportAirspace():
    """Exports the Airspace features as JSON."""
    airspaces = QgsProject.instance().mapLayersByName('Airspace')

    if not airspaces:
        QMessageBox.information(None, 'QgsOpenScope', 'Couldn\'t find an \'Airspace\' layer.')
        return

    _copyToClipboard(AirspaceModel.export(airspaces[0]))
    QMessageBox.information(None, 'QgsOpenScope', 'Airspace JSON has been copied to the clipboard.')

def exportFixes():
    """Exports the Fixes features as JSON."""
    fixes = QgsProject.instance().mapLayersByName('Fixes')

    if not fixes:
        QMessageBox.information(None, 'QgsOpenScope', 'Couldn\'t find a \'Fixes\' layer.')
        return

    _copyToClipboard(FixModel.export(fixes[0]))
    QMessageBox.information(None, 'QgsOpenScope', 'Fixes JSON has been copied to the clipboard.')

def exportRestricted():
    """Exports the Restricted Airspace features as JSON."""
    restricted = QgsProject.instance().mapLayersByName('Restricted')

    if not restricted:
        QMessageBox.information(None, 'QgsOpenScope', 'Couldn\'t find a \'Restricted\' layer.')
        return

    _copyToClipboard(RestrictedModel.export(restricted[0]))
    QMessageBox.information(None, 'QgsOpenScope', 'Restricted Airspace JSON has been copied to the clipboard.')

def exportMaps():
    """Exports the Map layers as JSON."""
    mapsGroup = QgsProject.instance().layerTreeRoot().findGroup('Maps')

    if not mapsGroup:
        QMessageBox.information(None, 'QgsOpenScope', 'Couldn\'t find any Map layers.')
        return

    layers = list(map(lambda x: x.layer(), mapsGroup.children()))

    _copyToClipboard(MapModel.export(layers))
    QMessageBox.information(None, 'QgsOpenScope', 'Map JSON has been copied to the clipboard.')

def exportTerrain(layers, fileName):
    """Exports the Terrain as GeoJSON."""

    if not fileName:
        fileName, _ = QFileDialog.getSaveFileName(None, 'Save openScope terrain', '', 'Terrain Files (*.geojson)')

    if not fileName:
        return

    result = processing.run('qgis:mergevectorlayers', {
        'LAYERS': layers,
        'OUTPUT': 'memory:'
    })
    merged = result['OUTPUT']
    merged.setName('Terrain - Merged')

    QgsVectorFileWriter.writeAsVectorFormat(
        merged,
        fileName,
        'utf-8',
        merged.crs(),
        'GeoJson',
        attributes=[
            merged.fields().indexFromName('elevation') # Only the elevation layer
        ],
        layerOptions=[
            'COORDINATE_PRECISION=%d' % EXPORT_PRECISION
        ]
    )

#------------------- Private -------------------

def _copyToClipboard(text):
    """Copies the specified text to the clipboard."""
    cb = QApplication.clipboard()
    cb.clear(mode=cb.Clipboard)
    cb.setText(text, mode=cb.Clipboard)
