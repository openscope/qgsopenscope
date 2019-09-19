import json
from qgis.core import QgsFeature, QgsField, QgsGeometry, QgsVectorLayer
from .functions import fromPolygon, toPolygon

class AirspaceModel:
    airspaceClass = None

    ceiling = None

    floor = None

    name = None

    poly = []

    def __init__(self, json):
        self.airspaceClass = json['airspace_class']
        self.ceiling = json['ceiling']
        self.floor = json['floor']
        self.name = None # json['name']
        self.poly = toPolygon(json['poly'])

    @staticmethod
    def export(layer):
        lines = []

        # Sort in order of area, largest first
        for f in sorted(layer.getFeatures(), key = lambda x : -x.geometry().area()):
            # The formatted list of lines
            poly = fromPolygon(f)
            pointLines = list(map(lambda x : '        ' + json.dumps(x), poly))

            template = """{
    "floor": %(floor)d,
    "ceiling": %(ceiling)d,
    "airspace_class": %(airspace_class)s,
    "poly": [
%(poly)s
    ]
}"""
            
            lines.append(template % {
                'floor': f['floor'],
                'ceiling': f['ceiling'],
                'airspace_class': json.dumps(f['airspace_class']),
                'poly': ',\n'.join(pointLines)
            })

        return ',\n'.join(lines)
