import json
from qgis.core import QgsFeature, QgsGeometry, QgsVectorLayer
from .functions import getOpenScopeLatLng, parseCoordinatesList

class Map:
    lines = []

    name = None

    def __init__(self, name, lines):
        self.lines =  parseCoordinatesList(lines)
        self.name = name

    @staticmethod
    def export(layers):
        lines = []

        for l in layers:
            # The formatted list of lines
            poly = []
            for f in l.getFeatures():
                points = f.geometry().asPolyline()
                count = len(points)
                i = 0
                while i < count - 1:
                    poly.append(getOpenScopeLatLng(points[i]) + getOpenScopeLatLng(points[i + 1]))
                    i += 1

            pointLines = list(map(lambda x : '        ' + json.dumps(x), poly))

            template = """{
    "name": %(name)s,
    "lines": [
%(lines)s
    ]
}"""
            
            lines.append(template % {
                'name': json.dumps(l.name()),
                'lines': ',\n'.join(pointLines)
            })

        return ',\n'.join(lines)