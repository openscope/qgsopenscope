"""An openScope airspace object."""
import json
from .functions import fromPolygon, toPolygon

class AirspaceModel:
    """An openScope airspace object."""

    airspaceClass = None

    ceiling = None

    floor = None

    name = None

    poly = []

    def __init__(self, value):
        self.airspaceClass = value['airspace_class']
        self.ceiling = value['ceiling']
        self.floor = value['floor']
        self.name = None # value['name']
        self.poly = toPolygon(value['poly'])

    @staticmethod
    def export(layer):
        """Export the specified QgsMapLayer features to JSON"""

        lines = []

        # Sort in order of area, largest first
        for f in sorted(layer.getFeatures(), key=lambda x: -x.geometry().area()):
            # The formatted list of lines
            poly = fromPolygon(f)
            pointLines = list(map(lambda x: '        ' + json.dumps(x), poly))

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
