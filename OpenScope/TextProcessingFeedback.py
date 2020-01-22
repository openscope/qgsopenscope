"""An extended feedback class"""
from qgis.PyQt.QtCore import pyqtSignal, QVariant
from qgis.core import QgsProcessingFeedback

class TextProcessingFeedback(QgsProcessingFeedback):
    """A custom feedback"""
    _progressText = None

    progressTextChanged = pyqtSignal(QVariant)

    def progressText(self):
        """Gets the progress text"""
        return self._progressText

    def setProgressText(self, text):
        """Sets the progress text"""
        self._progressText = text

        self.progressTextChanged.emit(text)
