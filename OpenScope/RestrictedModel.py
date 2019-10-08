"""An openScope Restricted Airspace object."""
import json
from .utilities.converters import fromPolygon, toPolygon

class RestrictedModel:
    """An openScope Restricted Airspace object."""

    height = None

    name = None

    coordinates = []

    def __init__(self, value):
        self.height = value['height']
        self.name = value['name']
        self.coordinates = toPolygon(value['coordinates'])

    @staticmethod
    def export(layer):
        """Export the specified QgsMapLayer features to JSON"""

        lines = []

        # Sort restricted airspace in order of name
        for f in sorted(layer.getFeatures(), key=lambda x: x['name']):
            # The formatted list of lines
            coordinates = fromPolygon(f)
            pointLines = list(map(lambda x: '        ' + json.dumps(x), coordinates))

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
