# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsOpenScopeDialog
                                 A QGIS plugin
 A collection of tools for the openScope project

 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-09-13
        git sha              : $Format:%H$
        copyright            : (C) 2019 by openScope
        email                : 3430117+oobayly@users.noreply.github.com

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import tempfile

from qgis.core import QgsSettings
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings_dialog_base.ui'))


class SettingsDialog(QtWidgets.QDialog, FORM_CLASS):
    """The dialog used for configuring settings."""

    _airport = None

    def __init__(self, parent=None):
        """Constructor."""
        super(SettingsDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.txtAirportPath.setText(SettingsDialog.getAirportPath())
        self.txtTempPath.setText(SettingsDialog.getTempPath())
        self.txtGSHHS.setText(SettingsDialog.getGSHHSPath())

        self.butSelectAirport.clicked.connect(self._butSelectAirportClicked)
        self.butSelectTemp.clicked.connect(self._butSelectTempClicked)
        self.butSelectGSHHS.clicked.connect(self._butSelectGSHHSClicked)

        self.buttonBox.accepted.connect(self._buttonBoxAccepted)
        self.buttonBox.rejected.connect(self._buttonBoxRejected)

    def _buttonBoxAccepted(self):
        """Handler for when the button box is accepted."""

        SettingsDialog.setAirportPath(self.txtAirportPath.text())
        SettingsDialog.setGSHHSPath(self.txtGSHHS.text())
        SettingsDialog.setTempPath(self.txtTempPath.text())

    def _buttonBoxRejected(self):
        """Handler for when the button box is accepted."""

    def _butSelectAirportClicked(self, _e):
        """Handler for when the Select Airport button is clicked."""
        directory = QFileDialog.getExistingDirectory(
            None,
            'Select Airport Directory',
            self.txtAirportPath.text()
        )

        if directory:
            self.txtAirportPath.setText(directory)
            SettingsDialog.setAirportPath(directory)

    def _butSelectGSHHSClicked(self, _e):
        """Handler for when the Select GSHHG button is clicked."""
        directory = QFileDialog.getExistingDirectory(
            None,
            'Select GSHHS Directory',
            self.txtGSHHS.text()
        )

        if directory:
            self.txtGSHHS.setText(directory)
            SettingsDialog.setGSHHSPath(directory)

    def _butSelectTempClicked(self, _e):
        """Handler for when the Select Temp button is clicked."""
        directory = QFileDialog.getExistingDirectory(
            None,
            'Select Temp Directory',
            self.txtTempPath.text()
        )

        if directory:
            self.txtTempPath.setText(directory)
            SettingsDialog.setTempPath(directory)

    @staticmethod
    def _readSetting(key, defaultValue=None):
        """Read the setting with specified key."""
        s = QgsSettings()

        return s.value('QgsOpenScope/%s' % key, defaultValue)

    @staticmethod
    def _saveSetting(key, value):
        """Saves  the setting with specified key."""
        s = QgsSettings()

        s.setValue('QgsOpenScope/%s' % key, value)

    @staticmethod
    def getAirportPath():
        """Gets the Airports path"""
        return SettingsDialog._readSetting('airportPath')

    @staticmethod
    def getGSHHSPath():
        """Gets the GSHHS path"""
        return SettingsDialog._readSetting('gshhsPath')

    @staticmethod
    def getTempPath():
        """Gets the temp path"""
        return SettingsDialog._readSetting('tempPath', tempfile.tempdir)

    @staticmethod
    def setAirportPath(path):
        """sets the Airports path"""
        SettingsDialog._saveSetting('airportPath', path)

    @staticmethod
    def setGSHHSPath(path):
        """Sets the GSHHS path"""
        SettingsDialog._saveSetting('gshhsPath', path)

    @staticmethod
    def setTempPath(path):
        """Sets the temp path"""
        SettingsDialog._saveSetting('tempPath', path)