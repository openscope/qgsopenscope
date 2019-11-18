"""A collection of UI utilities"""
import os
from qgis.PyQt import uic

_UI_PATH = '../resources/ui/'

def loadUIFormClass(uiFile):
    """Loads the specified UI file"""

    FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), _UI_PATH, '%s.ui' % uiFile))

    return FORM_CLASS
