import json
from qgis.core import QgsFeature, QgsGeometry, QgsVectorLayer
from .functions import getOpenScopeLatLng, parseCoordinates

class Fix:
    location = None

    name = None

    def __init__(self, name, location):
        self.location = parseCoordinates(location)[0]
        self.name = name

    @staticmethod
    def export(layer):
        features = {}
        for feature in layer.getFeatures():
            features[feature['name']] = feature

        # Custom sorting, so underscore is before letters
        keys = sorted(features.keys(), key = lambda x : x.replace('_', ' '))

        # To conform with the airport.json style guide
        lines = []
        for k in keys:
            f = features[k]
            p = f.geometry()
            spaces = ' ' * max(0, 5 - len(k))
            lines.append('    %(name)s%(spaces)s: %(coords)s' % {
                'name': json.dumps(k),
                'spaces': spaces,
                'coords': json.dumps(getOpenScopeLatLng(p.asPoint()))
            })

        template = """{
%s
}"""

        return template % ',\n'.join(lines)

