import json
from qgis.core import QgsFeature, QgsGeometry, QgsVectorLayer
from .functions import fromPolylines, toPolyline

class Map:
    lines = []

    name = None

    def __init__(self, name, lines):
        self.lines =  toPolyline(lines)
        self.name = name

    @staticmethod
    def export(layers):
        lines = []

        # Sort maps in order of name
        for l in sorted(layers, key = lambda x: x.name()):
            # The formatted list of lines
            poly = fromPolylines(l.getFeatures())

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