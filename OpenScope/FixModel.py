import json
from qgis.core import QgsFeature, QgsGeometry, QgsVectorLayer
from .functions import fromPointXY, toPointXY

class FixModel:
    location = None

    name = None

    def __init__(self, name, location):
        self.location = toPointXY(location)
        self.name = name

    @staticmethod
    def export(layer):
        lines = []

        # Sort fixes in order of name, but place underscores at the top
        for f in sorted(layer.getFeatures(), key = lambda x: x['name'].replace('_', ' ')):
            name = f['name']
            spaces = ' ' * max(0, 5 - len(name))
            lines.append('    %(name)s%(spaces)s: %(coords)s' % {
                'name': json.dumps(name),
                'spaces': spaces,
                'coords': json.dumps(fromPointXY(f.geometry().asPoint()))
            })

        template = """{
%s
}"""

        return template % ',\n'.join(lines)

