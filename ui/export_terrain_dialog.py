"""The dialog used for editing the plugin configuration"""
#pylint: disable=broad-except

from qgis.PyQt import  QtCore, QtWidgets
from qgis.PyQt.QtWidgets import QDialogButtonBox, QFileDialog, QListWidgetItem
from qgis.core import (
    QgsMapLayer,
    QgsProject,
    QgsWkbTypes
)
from .ui_utils import loadUIFormClass
from ..OpenScope.utilities.exporter import exportTerrain

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS = loadUIFormClass('export_terrain_dialog')

class ExportTerrainDialog(QtWidgets.QDialog, FORM_CLASS):
    """The dialog used for exporting terrain."""

    def __init__(self, parent=None):
        """Constructor."""

        super(ExportTerrainDialog, self).__init__(parent)

        self.setupUi(self)

        self._populateTerrainLayers()

        self.butSelectTerrainFile.clicked.connect(self._butSelectTerrainFileClicked)
        self.listLayers.itemSelectionChanged.connect(self._listLayersItemSelectionChanged)

        self.buttonBox.accepted.connect(self._buttonBoxAccepted)
        self.buttonBox.rejected.connect(self._buttonBoxRejected)

        self._onInputStateChanged()

#------------------- Event handlers -------------------

    def _buttonBoxAccepted(self):
        """Handler for when the button box is accepted."""

        fileName = self.txtTerrainFile.text()
        layers = list(map(
            lambda x: x.data(QtCore.Qt.UserRole),
            self.listLayers.selectedItems()
        ))

        exportTerrain(layers, fileName)

    def _buttonBoxRejected(self):
        """Handler for when the button box is accepted."""

    def _butSelectTerrainFileClicked(self, _e):
        """Handler for when the Select Terrain button is clicked."""

        fileName, _ = QFileDialog.getSaveFileName(None, 'Select openScope terrain', '', 'Terrain Files (*.geojson)')

        self.txtTerrainFile.setText(fileName)

        self._onInputStateChanged()

    def _listLayersItemSelectionChanged(self):
        """Handler for when the layers list selection changes"""
        self._onInputStateChanged()

#------------------- Private -------------------

    def _onInputStateChanged(self):
        """Handles when the dialog inputs change"""

        fileName = self.txtTerrainFile.text()
        isFileValid = True
        layerCount = len(self.listLayers.selectedItems())

        try:
            open(fileName, 'w')
        except OSError:
            isFileValid = False

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(isFileValid and layerCount)

    def _populateTerrainLayers(self):
        """Populates the layers list"""

        listLayers = self.listLayers

        listLayers.clear()

        for layerView in QgsProject.instance().layerTreeRoot().findLayers():
            layer = layerView.layer()

            # Must be vectory
            if layer.type() != QgsMapLayer.VectorLayer:
                continue

            # Must be polygon
            if layer.geometryType() != QgsWkbTypes.PolygonGeometry:
                continue

            fields = layer.fields()
            elevationIndex = fields.indexOf('elevation')

            if elevationIndex == -1:
                continue

            listItem = QListWidgetItem(listLayers)
            listItem.setText(layer.name())
            listItem.setData(QtCore.Qt.UserRole, layer)
