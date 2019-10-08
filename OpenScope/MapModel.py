"""An openScope Map object."""
import json
from .utilities.converters import fromPolylines, toPolyline

class MapModel:
    """An openScope Map object."""

    lines = []

    name = None

    def __init__(self, name, lines):
        self.lines = toPolyline(lines)
        self.name = name

    @staticmethod
    def export(layers):
        """Export the specified QgsMapLayer features to JSON"""

        lines = []

        # Sort maps in order of name
        for l in sorted(layers, key=lambda x: x.name()):
            # The formatted list of lines
            poly = fromPolylines(l.getFeatures())

            pointLines = list(map(lambda x: '        ' + json.dumps(x), poly))

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
