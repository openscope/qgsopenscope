"""The dialog used for editing the plugin configuration"""
#pylint: disable=broad-except

import os

from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QDialogButtonBox, QFileDialog, QMessageBox
from ..OpenScope.AirportModel import AirportModel
from ..OpenScope.ProjectGenerator import LayerType, ProjectGenerator, ProjectGeneratorConfig
from .settings_dialog import SettingsDialog
from .ui_utils import loadUIFormClass

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS = loadUIFormClass('import_dialog')

class ImportDialog(QtWidgets.QDialog, FORM_CLASS):
    """The dialog used for importing an airport."""

    def __init__(self, parent=None):
        """Constructor."""

        super(ImportDialog, self).__init__(parent)

        self.setupUi(self)

        self._setAirportFile(SettingsDialog.getLastAirportPath())

        self.checkMaps.stateChanged.connect(self._checkMapsStateChanged)
        self.butSelectAirportFile.clicked.connect(self._butSelectAirportFileClicked)

        self.buttonBox.accepted.connect(self._buttonBoxAccepted)
        self.buttonBox.rejected.connect(self._buttonBoxRejected)

#------------------- Event handlers -------------------

    def _buttonBoxAccepted(self):
        """Handler for when the button box is accepted."""

        config = self._buildConfiguration()

        try:
            proj = ProjectGenerator(config)
            proj.populateProject()
            proj.saveProject()
        except Exception as e:
            QMessageBox.warning(None, 'QgsOpenScope', str(e))

    def _buttonBoxRejected(self):
        """Handler for when the button box is accepted."""

    def _butSelectAirportFileClicked(self, _e):
        """Handler for when the Select Airport button is clicked."""

        fileName, _ = QFileDialog.getOpenFileName(
            None,
            'Load openScope Airport',
            SettingsDialog.getLastAirportPath(),
            'Airport Files(*.json)',
        )

        if not fileName:
            return

        if not os.path.isfile(fileName):
            QMessageBox.warning(None, 'QgsOpenScope', 'Airport File \'%s\' does not exist.' % fileName)
            return

        self._setAirportFile(fileName)
        SettingsDialog.setLastAirportPath(fileName)

    def _checkMapsStateChanged(self, _e):
        """Handler for when the Maps checkbox state is changed"""

        self.listMaps.setEnabled(self.checkMaps.isChecked())

#------------------- Private -------------------

    def _buildConfiguration(self):
        """Builds the ProjectGeneratorConfig"""

        config = ProjectGeneratorConfig()

        config.airportFile = self.txtAirportFile.text()
        config.projectPath = SettingsDialog.getProjectPath()
        config.tmpPath = SettingsDialog.getTempPath()

        if self.checkFixes.isChecked():
            config.layers = config.layers | LayerType.Fixes

        if self.checkRestrictedAirspace.isChecked():
            config.layers = config.layers | LayerType.Restricted

        if self.checkAirspace.isChecked():
            config.layers = config.layers | LayerType.Airspace

        if self.checkAirspaceHidden.isChecked():
            config.layers = config.layers | LayerType.AirspaceHidden

        if self.checkMaps.isChecked():
            config.layers = config.layers | LayerType.Maps

        config.mapNames = list(map(
            lambda x: x.text(),
            self.listMaps.selectedItems()
        ))

        return config

    @staticmethod
    def _configureCheckbox(checkbox, count, text, pluralSuffix='s', layerType=LayerType.Empty):
        """Configures the checkbox for display"""

        hasExisting = ProjectGenerator.hasExistingLayers(layerType)
        label = '%d %s%s' % (
            count,
            text,
            '' if count == 1 else pluralSuffix
        )

        checkbox.setProperty('hasLayer', hasExisting)
        checkbox.setText(label)
        checkbox.setEnabled(count != 0)
        checkbox.setChecked(count != 0)

    def _configureMapList(self, mapNames):
        """Configures the map listwidget"""

        self.listMaps.clear()
        self.listMaps.addItems(mapNames)
        self.listMaps.selectAll()
        self.listMaps.setEnabled(len(mapNames) != 0)

    def _setAirportFile(self, fileName):
        """Sets the airport filename for the dialog"""

        self.txtAirportFile.setText(fileName)

        icao = 'No Airport Loaded'
        airport = None
        fixes = 0
        restricted = 0
        airspace = 0
        airspaceHidden = 0
        mapNames = []

        try:
            airport = AirportModel(fileName)
            icao = 'Loaded %s' % airport.getIcao()
            airspace = len(airport.getAirspace())
            airspaceHidden = len(airport.getAirspace(True))
            fixes = len(airport.getFixes())
            mapNames = list(map(lambda x: x.name, airport.getMaps()))
            restricted = len(airport.getRestricted())

        except Exception as e:
            QMessageBox.warning(None, 'QgsOpenScope', str(e))

        self.lblICAO.setText(icao)

        ImportDialog._configureCheckbox(
            self.checkAirspace, airspace,
            'Airspace',
            layerType=LayerType.Airspace
        )
        ImportDialog._configureCheckbox(
            self.checkAirspaceHidden, airspaceHidden,
            'Hidden Airspace',
            layerType=LayerType.AirspaceHidden
        )
        ImportDialog._configureCheckbox(
            self.checkFixes, fixes,
            'Fix', 'es',
            layerType=LayerType.Fixes
        )
        ImportDialog._configureCheckbox(
            self.checkMaps, len(mapNames),
            'Map',
            layerType=LayerType.Maps
        )
        ImportDialog._configureCheckbox(
            self.checkRestrictedAirspace, restricted,
            'Restricted Airspace',
            layerType=LayerType.Restricted
        )

        self._configureMapList(mapNames)

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(airport is not None)
