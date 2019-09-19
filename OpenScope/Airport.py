import re
import json
import numpy
from qgis.core import QgsPointXY
from .Airspace import Airspace
from .Fix import Fix
from .Map import Map
from .Restricted import Restricted

# An openScope airport object
class Airport:
    _airport = None

    # Initializes the airport object
    def __init__(self, path):
        self._loadAirport(path)

    # Load the openScopeAirport from the specified file
    def _loadAirport(self, path):
        with open(path, 'r') as f:
            self._airport = json.load(f)

    def getAirspace(self):
        return list(map(lambda item: Airspace(item), self._airport['airspace']))

    def getIcao(self):
        return self._airport['icao']
    
    def getFixes(self):
        fixes = []

        for key, value in self._airport['fixes'].items():
            fixes.append(Fix(key, value))
        
        return fixes

    def getMaps(self):
        maps = []

        mapsJson = self._airport['maps']
        if type(mapsJson) is dict:
            for key, value in mapsJson.items():
                maps.append(Map(key, value))

        else:
            for value in mapsJson:
                maps.append(Map(value['name'], value['lines']))
        
        return maps

    def getRestricted(self):
        return list(map(
            lambda item: Restricted(item),
            self._airport.get('restricted') or []
        ))
