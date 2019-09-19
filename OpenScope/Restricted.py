import json
from qgis.core import QgsFeature, QgsField, QgsGeometry, QgsVectorLayer
from .functions import fromPolygon, toPolygon

class Restricted:
    height = None

    name = None

    coordinates = []

    def __init__(self, json):
        self.height = json['height']
        self.name = json['name']
        self.coordinates = toPolygon(json['coordinates'])

    @staticmethod
    def export(layer):
        lines = []

        # Sort restricted airspace in order of name
        for f in sorted(layer.getFeatures(), key = lambda x : x['name']):
            # The formatted list of lines
            coordinates = fromPolygon(f)
            pointLines = list(map(lambda x : '        ' + json.dumps(x), coordinates))

            template = """{
    "name": %(name)s,
    "height": %(height)s,
    "coordinates": [
%(coordinates)s
    ]
}"""
            
            lines.append(template % {
                'name': json.dumps(f['name']),
                'height': json.dumps(f['height']),
                'coordinates': ',\n'.join(pointLines)
            })

        return ',\n'.join(lines)
