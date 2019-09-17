from qgis.core import QgsFeature, QgsField, QgsGeometry, QgsVectorLayer
from PyQt5.QtCore import QVariant
from .functions import parseCoordinatesList

class Restricted:
    height = None

    name = None

    poly = []

    def __init__(self, json):
        self.height = json['height']
        self.name = json['name']
        self.poly = list(map(lambda item: item[0], parseCoordinatesList(json['coordinates'])))
