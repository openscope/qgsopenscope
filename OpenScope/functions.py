import re
from qgis.core import QgsPointXY

_LAT_LNG = re.compile(r'^([NESW])(\d+(\.\d+)?)([d °](\d+(\.\d+)?))?([m \'](\d+(\.\d+)?))?$', re.IGNORECASE)
_SW = re.compile('[SW]', re.IGNORECASE)

# Closes the specifeid polygon
def _closePoly(poly):
    first = poly[0]
    last = poly[-1]

    if ((first.x != last.x) or (first.y != last.y)):
        poly.append(first)

def getOpenScopeLatLng(point):
    lat = point.y()
    lng = point.x()
    ns = 'S' if lat < 0 else 'N'
    ew = 'W' if lng < 0 else 'E'

    return [
        ns + '%02.8f' % abs(lat),
        ew + '%03.8f' % abs(lng),
    ]

# This emulates openScope's unitConverter.parseCoordinate method
def parseCoordinateValue(value):
    if (isinstance(value, float) or isinstance(value, float)):
        return value

    match = _LAT_LNG.match(str(value))
    if (match == None):
        raise(Exception('Cannot parse %s as coordinate' % value))
    
    degrees = float(match.group(2))
    minutes = 0
    seconds = 0
    if (match.group(5) != None):
        minutes = float(match.group(5)) / 60

    if (match.group(8) != None):
        seconds = float(match.group(8)) / 3600
    
    decimalDegrees = degrees + minutes + seconds

    if (_SW.match(match.group(1))):
        decimalDegrees *= -1

    return decimalDegrees

# Parse a list of coordinate values
def parseCoordinates(coords):
    i = 0
    limit = len(coords) - 1
    resp = []
    while i < limit:
        resp.append(QgsPointXY(
            parseCoordinateValue(coords[i + 1]),
            parseCoordinateValue(coords[i + 0])
        ))

        i += 2

    return resp

# Parse a 2d list of coordinates
def parseCoordinatesList(values):
    return list(map(lambda vals: parseCoordinates(vals), values))
