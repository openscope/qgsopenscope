"""An openScope airport"""
import json
from .AirspaceModel import AirspaceModel
from .FixModel import FixModel
from .MapModel import MapModel
from .RestrictedModel import RestrictedModel

class AirportModel:
    """An openScope airport"""

    _airport = None

    # Initializes the airport object
    def __init__(self, path):
        self._loadAirport(path)

    def _loadAirport(self, path):
        """Loads the aiport from the specified file."""

        with open(path, 'r') as f:
            self._airport = json.load(f)

    def getAirspace(self, hiddenAirspace=False):
        """Gets the list of AirspaceModel objects."""

        sectionName = '_airspace' if hiddenAirspace else 'airspace'

        return [
            AirspaceModel(item)
            for item in self._airport[sectionName]
        ]

    def getIcao(self):
        """Gets the ICAO code for the airport."""

        return self._airport['icao']

    def getFixes(self):
        """Gets the list of FixModel objects."""

        return [
            FixModel(key, value)
            for key, value in self._airport['fixes'].items()
        ]

    def getMaps(self):
        """Gets the list of MapModel objcets."""

        maps = []

        mapsJson = self._airport['maps']
        if isinstance(mapsJson, dict):
            for key, value in mapsJson.items():
                maps.append(MapModel(key, value))

        else:
            for value in mapsJson:
                maps.append(MapModel(value['name'], value['lines']))

        return maps

    def getRestricted(self):
        """Gets the list of RestrictedModel objects."""

        return [
            RestrictedModel(item)
            for item in self._airport.get('restricted') or []
        ]
