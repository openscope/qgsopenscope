"""A collection of drawing functions"""
import math
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsDistanceArea,
    QgsFeature,
    QgsGeometry,
    QgsProject,
    QgsWkbTypes
)
from qgis.utils import iface

_EPSG_4326 = wgs = QgsCoordinateReferenceSystem('EPSG:4326') # WGS84
_EPSG_4326_SRS_ID = 3452
_METRES_PER_NM = 1852
_MIN_ANGLE = 2 * math.pi / 36 # Minimum segment angle
_MIN_CIRCLE_SEGMENTS = 36
_MIN_SEGMENT_LENGTH = 1

#------------------- Public -------------------

def drawCircles(radius, points=None, layer=None):
    """Draws a circle of `radius` NM around the specified QgsPointXY(s)"""

    canvas, layer, message = _validateCanvasAndLayer(layer)
    if not canvas:
        return (False, message)

    if not points:
        points = _getSelectedPoints()

    if not points:
        return (False, 'No points are selected')

    da = _getDistanceArea()

    for p in points:
        _drawCircle(radius, p, layer, da)

    canvas.refreshAllLayers()

    return (True, None)

def drawRunwayExtension(length, dashLength=1, crossInterval=4, crossWidth=1, features=None, layer=None):
    """Draw the runway extension lines """

    canvas, layer, message = _validateCanvasAndLayer(layer)
    if not canvas:
        return (False, message)

    if not features:
        features = _getSelectedFeatures()

    if not features:
        return (False, 'No features selected')

    points = filter(
        lambda x: x.geometry().type() == QgsWkbTypes.PointGeometry,
        features
    )

    points = list(map(
        lambda x: x.geometry().asPoint(),
        points
    ))

    lines = list(filter(
        lambda x: x.geometry().type() == QgsWkbTypes.LineGeometry,
        features
    ))

    if points and lines:
        return (False, 'Ambigious selection. Please select a line OR two points')

    if points:
        if len(points) != 2:
            return (False, 'Exactly two points must be selected')

    else:
        if len(lines) != 1:
            return (False, 'Exactly one line segment must be selected')

        points = lines[0].geometry().asPolyline()

        if len(points) != 2:
            return (False, 'A line segment with exactly two points must be selected')

    da = _getDistanceArea()

    _drawRunwayExtension(length, dashLength, crossInterval, crossWidth, points, layer, da)

    canvas.refreshAllLayers()

    return (True, None)

#------------------- Private -------------------

def _drawCircle(radius, centre, layer, da):
    """Draws a circle of `radius` NM around the specified QgsPointXY"""

    # Number of line segments to give _MIN_SEGMENT_LENGTH NM
    segments = max(
        math.ceil(2 * radius * math.pi),
        _MIN_CIRCLE_SEGMENTS
    )

    angle = 2 * math.pi / segments

    radius *= _METRES_PER_NM

    i = 0
    points = []
    while i < segments:
        points.append(da.computeSpheroidProject(centre, radius, i * angle))
        i += 1

    points.append(points[0])

    feature = QgsFeature(layer.fields())
    feature.setGeometry(QgsGeometry.fromPolylineXY(points))
    layer.dataProvider().addFeatures([feature])

def _drawRunwayExtension(length, dashLength, crossInterval, crossWidth, points, layer, da):
    """Draw the runway extension lines """

    bearing = da.bearing(points[0], points[1])

    features = []
    features.extend(_generateRunwayExtension(
        points[0],
        bearing + math.pi,
        length,
        dashLength,
        crossInterval,
        crossWidth,
        da
    ))
    features.extend(_generateRunwayExtension(
        points[1],
        bearing,
        length,
        dashLength,
        crossInterval,
        crossWidth,
        da
    ))

    layer.dataProvider().addFeatures(features)

def _generateRunwayExtension(origin, bearing, length, dashLength, crossInterval, crossWidth, da):
    """Generates the features for"""
    i = 0
    features = []

    tOffset = crossWidth * _METRES_PER_NM / 2
    dashLength *= _METRES_PER_NM / 2

    while i < length:
        l0 = da.computeSpheroidProject(origin, dashLength * ((2 * i) + 1), bearing)
        l1 = da.computeSpheroidProject(origin, dashLength * ((2 * i) + 2), bearing)
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolylineXY([l0, l1]))
        features.append(feat)

        if i > 0 and i % crossInterval == crossInterval -1:
            x0 = da.computeSpheroidProject(l1, tOffset, bearing - (math.pi / 2))
            x1 = da.computeSpheroidProject(l1, tOffset, bearing + (math.pi / 2))
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPolylineXY([x0, x1]))
            features.append(feat)

        i += 1

    return features

def _getDistanceArea():
    """Gets tje tool used to calculate distances, bearings and offset points"""
    da = QgsDistanceArea()
    da.setSourceCrs(_EPSG_4326, QgsProject.instance().transformContext())
    da.setEllipsoid(QgsProject.instance().ellipsoid())

    return da

def _getSelectedFeatures():
    """Gets all the selected features"""
    features = []

    for layer in QgsProject.instance().layerTreeRoot().findLayers():
        if not layer.layer().selectedFeatureCount():
            continue

        features.extend(layer.layer().selectedFeatures())

    return features

def _getSelectedLines():
    """Gets all the selected lines on all layers"""

    return list(filter(
        lambda x: x.geometry().type() == QgsWkbTypes.LineGeometry,
        _getSelectedFeatures()
    ))

def _getSelectedPoints():
    """Gets all the selected points on all layers"""

    features = filter(
        lambda x: x.geometry().type() == QgsWkbTypes.PointGeometry,
        _getSelectedFeatures()
    )

    return list(map(lambda x: x.geometry().asPoint(), features))

def _validateCanvasAndLayer(layer, requiredType=QgsWkbTypes.LineString):
    """Validates the canvas"""

    canvas = iface.mapCanvas()

    if canvas.mapSettings().destinationCrs().srsid() != _EPSG_4326_SRS_ID:
        return (None, None, 'Cannot continue. Canvas needs to be using WGS84 (EPSG 4326)')

    if not layer:
        layer = iface.activeLayer()

    if not layer or layer.wkbType() != requiredType:
        return (
            None,
            None,
            'Cannot draw lines on %s layer' % QgsWkbTypes.displayString(layer.wkbType())
        )

    return (canvas, layer, None)
