"""
The DEM tiles map

Run the following javascript in a console on this page
http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm


areas = Array.from(document.getElementsByTagName('area'))

const tiles = areas.map(item => {
    const coords = item.attributes['coords'].value.split(',').map(x => parseInt(x) / 5);
    const uri = item.attributes['href'].value;
    const name = item.attributes['title'].value;
    let [lng0, lat1, lng1, lat0] = coords;

    lng0 -= 180;
    lng1 -= 180;
    lat0 = 90 - lat0;
    lat1 = 90 - lat1;

    const area = Math.abs((lat1 - lat0) * (lng1 - lng0));

    return {
        lat0,
        lng0,
        lat1,
        lng1,
        uri,
        name,
        area
    };
});

copy(tiles);
"""

#pylint: disable=too-many-lines

import json

_DEM_TILES = json.loads("""[
  {
    "lat0": 80,
    "lng0": -102,
    "lat1": 84,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/U14.zip",
    "name": "U14",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": -96,
    "lat1": 84,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/U15.zip",
    "name": "U15",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": -90,
    "lat1": 84,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/U16.zip",
    "name": "U16",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": -84,
    "lat1": 84,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/U17.zip",
    "name": "U17",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": -78,
    "lat1": 84,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/U18.zip",
    "name": "U18",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": -72,
    "lat1": 84,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/U19.zip",
    "name": "U19",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": -66,
    "lat1": 84,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/U20.zip",
    "name": "U20",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": -60,
    "lat1": 84,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/U21.zip",
    "name": "U21",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": -54,
    "lat1": 84,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/U22.zip",
    "name": "U22",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 12,
    "lat1": 84,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "U33",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 18,
    "lat1": 84,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "U34",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 24,
    "lat1": 84,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "U35",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 30,
    "lat1": 84,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "U36",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 36,
    "lat1": 84,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/FJ.zip",
    "name": "U37",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 42,
    "lat1": 84,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/FJ.zip",
    "name": "U38",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 48,
    "lat1": 84,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/FJ.zip",
    "name": "U39",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 54,
    "lat1": 84,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/FJ.zip",
    "name": "U40",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 60,
    "lat1": 84,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/FJ.zip",
    "name": "U41",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 78,
    "lat1": 84,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/U44.zip",
    "name": "U44",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 90,
    "lat1": 84,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/U46.zip",
    "name": "U46",
    "area": 24
  },
  {
    "lat0": 80,
    "lng0": 96,
    "lat1": 84,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/U47.zip",
    "name": "U47",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -126,
    "lat1": 80,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/T10.zip",
    "name": "T10",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -120,
    "lat1": 80,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/T11.zip",
    "name": "T11",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -114,
    "lat1": 80,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/T12.zip",
    "name": "T12",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -108,
    "lat1": 80,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/T13.zip",
    "name": "T13",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -102,
    "lat1": 80,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/T14.zip",
    "name": "T14",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -96,
    "lat1": 80,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/T15.zip",
    "name": "T15",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -90,
    "lat1": 80,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/T16.zip",
    "name": "T16",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -84,
    "lat1": 80,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/T17.zip",
    "name": "T17",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -78,
    "lat1": 80,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/T18.zip",
    "name": "T18",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -72,
    "lat1": 80,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/T19.zip",
    "name": "T19",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 6,
    "lat1": 80,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "T32",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 12,
    "lat1": 80,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "T33",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 18,
    "lat1": 80,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "T34",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 24,
    "lat1": 80,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "T35",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 30,
    "lat1": 80,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SVALBARD.zip",
    "name": "T36",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 48,
    "lat1": 80,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/FJ.zip",
    "name": "T39",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 54,
    "lat1": 80,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/T40.zip",
    "name": "T40",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 60,
    "lat1": 80,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/T41.zip",
    "name": "T41",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 66,
    "lat1": 80,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/T42.zip",
    "name": "T42",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 72,
    "lat1": 80,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/T43.zip",
    "name": "T43",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 78,
    "lat1": 80,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/T44.zip",
    "name": "T44",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 84,
    "lat1": 80,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/T45.zip",
    "name": "T45",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 90,
    "lat1": 80,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/T46.zip",
    "name": "T46",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 96,
    "lat1": 80,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/T47.zip",
    "name": "T47",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 102,
    "lat1": 80,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/T48.zip",
    "name": "T48",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 108,
    "lat1": 80,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/T49.zip",
    "name": "T49",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 132,
    "lat1": 80,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/T53.zip",
    "name": "T53",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 138,
    "lat1": 80,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/T54.zip",
    "name": "T54",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 144,
    "lat1": 80,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/T55.zip",
    "name": "T55",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 150,
    "lat1": 80,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/T56.zip",
    "name": "T56",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": 156,
    "lat1": 80,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/T57.zip",
    "name": "T57",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -126,
    "lat1": 76,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/S10.zip",
    "name": "S10",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -120,
    "lat1": 76,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/S11.zip",
    "name": "S11",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -114,
    "lat1": 76,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/S12.zip",
    "name": "S12",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -108,
    "lat1": 76,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/S13.zip",
    "name": "S13",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -102,
    "lat1": 76,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/S14.zip",
    "name": "S14",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -96,
    "lat1": 76,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/S15.zip",
    "name": "S15",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -90,
    "lat1": 76,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/S16.zip",
    "name": "S16",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -84,
    "lat1": 76,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/S17.zip",
    "name": "S17",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": -78,
    "lat1": 76,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/S18.zip",
    "name": "S18",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 48,
    "lat1": 76,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/S39.zip",
    "name": "S39",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 54,
    "lat1": 76,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/S40.zip",
    "name": "S40",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 60,
    "lat1": 76,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/S41.zip",
    "name": "S41",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 66,
    "lat1": 76,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/S42.zip",
    "name": "S42",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 72,
    "lat1": 76,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/S43.zip",
    "name": "S43",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 78,
    "lat1": 76,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/S44.zip",
    "name": "S44",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 84,
    "lat1": 76,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/S45.zip",
    "name": "S45",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 90,
    "lat1": 76,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/S46.zip",
    "name": "S46",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 96,
    "lat1": 76,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/S47.zip",
    "name": "S47",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 102,
    "lat1": 76,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/S48.zip",
    "name": "S48",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 108,
    "lat1": 76,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/S49.zip",
    "name": "S49",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 114,
    "lat1": 76,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/S50.zip",
    "name": "S50",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 120,
    "lat1": 76,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/S51.zip",
    "name": "S51",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 126,
    "lat1": 76,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/S52.zip",
    "name": "S52",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 132,
    "lat1": 76,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/S53.zip",
    "name": "S53",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 138,
    "lat1": 76,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/S54.zip",
    "name": "S54",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 144,
    "lat1": 76,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/S55.zip",
    "name": "S55",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 150,
    "lat1": 76,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/S56.zip",
    "name": "S56",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -168,
    "lat1": 72,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/R03.zip",
    "name": "R03",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -162,
    "lat1": 72,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/R04.zip",
    "name": "R04",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -156,
    "lat1": 72,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/R05.zip",
    "name": "R05",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -150,
    "lat1": 72,
    "lng1": -144,
    "uri": "http://viewfinderpanoramas.org/dem3/R06.zip",
    "name": "R06",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -144,
    "lat1": 72,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/R07.zip",
    "name": "R07",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -138,
    "lat1": 72,
    "lng1": -132,
    "uri": "http://viewfinderpanoramas.org/dem3/R08.zip",
    "name": "R08",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -132,
    "lat1": 72,
    "lng1": -126,
    "uri": "http://viewfinderpanoramas.org/dem3/R09.zip",
    "name": "R09",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -126,
    "lat1": 72,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/R10.zip",
    "name": "R10",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -120,
    "lat1": 72,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/R11.zip",
    "name": "R11",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -114,
    "lat1": 72,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/R12.zip",
    "name": "R12",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -108,
    "lat1": 72,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/R13.zip",
    "name": "R13",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -102,
    "lat1": 72,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/R14.zip",
    "name": "R14",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -96,
    "lat1": 72,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/R15.zip",
    "name": "R15",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -90,
    "lat1": 72,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/R16.zip",
    "name": "R16",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -84,
    "lat1": 72,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/R17.zip",
    "name": "R17",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -78,
    "lat1": 72,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/R18.zip",
    "name": "R18",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -72,
    "lat1": 72,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/R19.zip",
    "name": "R19",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -66,
    "lat1": 72,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/R20.zip",
    "name": "R20",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 12,
    "lat1": 72,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/R33v2.zip",
    "name": "R33",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 18,
    "lat1": 72,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/R34v2.zip",
    "name": "R34",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 24,
    "lat1": 72,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/R35v2.zip",
    "name": "R35",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 30,
    "lat1": 72,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/R36v2.zip",
    "name": "R36",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 36,
    "lat1": 72,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/R37v2.zip",
    "name": "R37",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 42,
    "lat1": 72,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/R38v2.zip",
    "name": "R38",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 48,
    "lat1": 72,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/R39.zip",
    "name": "R39",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 54,
    "lat1": 72,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/R40.zip",
    "name": "R40",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 60,
    "lat1": 72,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/R41.zip",
    "name": "R41",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 66,
    "lat1": 72,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/R42.zip",
    "name": "R42",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 72,
    "lat1": 72,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/R43.zip",
    "name": "R43",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 78,
    "lat1": 72,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/R44.zip",
    "name": "R44",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 84,
    "lat1": 72,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/R45.zip",
    "name": "R45",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 90,
    "lat1": 72,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/R46.zip",
    "name": "R46",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 96,
    "lat1": 72,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/R47.zip",
    "name": "R47",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 102,
    "lat1": 72,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/R48.zip",
    "name": "R48",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 108,
    "lat1": 72,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/R49.zip",
    "name": "R49",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 114,
    "lat1": 72,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/R50.zip",
    "name": "R50",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 120,
    "lat1": 72,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/R51.zip",
    "name": "R51",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 126,
    "lat1": 72,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/R52.zip",
    "name": "R52",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 132,
    "lat1": 72,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/R53.zip",
    "name": "R53",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 138,
    "lat1": 72,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/R54.zip",
    "name": "R54",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 144,
    "lat1": 72,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/R55.zip",
    "name": "R55",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 150,
    "lat1": 72,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/R56.zip",
    "name": "R56",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 156,
    "lat1": 72,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/R57.zip",
    "name": "R57",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 162,
    "lat1": 72,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/R58.zip",
    "name": "R58",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 168,
    "lat1": 72,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/R59.zip",
    "name": "R59",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": 174,
    "lat1": 72,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/R60.zip",
    "name": "R60",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -180,
    "lat1": 72,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/R01.zip",
    "name": "R01",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -168,
    "lat1": 68,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/Q03.zip",
    "name": "Q03",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -162,
    "lat1": 68,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/Q04.zip",
    "name": "Q04",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -156,
    "lat1": 68,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/Q05.zip",
    "name": "Q05",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -150,
    "lat1": 68,
    "lng1": -144,
    "uri": "http://viewfinderpanoramas.org/dem3/Q06.zip",
    "name": "Q06",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -144,
    "lat1": 68,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/Q07.zip",
    "name": "Q07",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -138,
    "lat1": 68,
    "lng1": -132,
    "uri": "http://viewfinderpanoramas.org/dem3/Q08.zip",
    "name": "Q08",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -132,
    "lat1": 68,
    "lng1": -126,
    "uri": "http://viewfinderpanoramas.org/dem3/Q09.zip",
    "name": "Q09",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -126,
    "lat1": 68,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/Q10.zip",
    "name": "Q10",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -120,
    "lat1": 68,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/Q11.zip",
    "name": "Q11",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -114,
    "lat1": 68,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/Q12.zip",
    "name": "Q12",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -108,
    "lat1": 68,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/Q13.zip",
    "name": "Q13",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -102,
    "lat1": 68,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/Q14.zip",
    "name": "Q14",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -96,
    "lat1": 68,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/Q15.zip",
    "name": "Q15",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -90,
    "lat1": 68,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/Q16.zip",
    "name": "Q16",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -84,
    "lat1": 68,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/Q17.zip",
    "name": "Q17",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -78,
    "lat1": 68,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/Q18.zip",
    "name": "Q18",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -72,
    "lat1": 68,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/Q19.zip",
    "name": "Q19",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -66,
    "lat1": 68,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/Q20.zip",
    "name": "Q20",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 6,
    "lat1": 68,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/Q32v2.zip",
    "name": "Q32",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 12,
    "lat1": 68,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/Q33v2.zip",
    "name": "Q33",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 18,
    "lat1": 68,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/Q34v2.zip",
    "name": "Q34",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 24,
    "lat1": 68,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/Q35v2.zip",
    "name": "Q35",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 30,
    "lat1": 68,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/Q36v2.zip",
    "name": "Q36",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 36,
    "lat1": 68,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/Q37v2.zip",
    "name": "Q37",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 42,
    "lat1": 68,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/Q38v2.zip",
    "name": "Q38",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 48,
    "lat1": 68,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/Q39v2.zip",
    "name": "Q39",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 54,
    "lat1": 68,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/Q40v2.zip",
    "name": "Q40",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 60,
    "lat1": 68,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/Q41.zip",
    "name": "Q41",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 66,
    "lat1": 68,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/Q42.zip",
    "name": "Q42",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 72,
    "lat1": 68,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/Q43.zip",
    "name": "Q43",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 78,
    "lat1": 68,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/Q44.zip",
    "name": "Q44",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 84,
    "lat1": 68,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/Q45.zip",
    "name": "Q45",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 90,
    "lat1": 68,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/Q46.zip",
    "name": "Q46",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 96,
    "lat1": 68,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/Q47.zip",
    "name": "Q47",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 102,
    "lat1": 68,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/Q48.zip",
    "name": "Q48",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 108,
    "lat1": 68,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/Q49.zip",
    "name": "Q49",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 114,
    "lat1": 68,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/Q50.zip",
    "name": "Q50",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 120,
    "lat1": 68,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/Q51.zip",
    "name": "Q51",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 126,
    "lat1": 68,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/Q52.zip",
    "name": "Q52",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 132,
    "lat1": 68,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/Q53.zip",
    "name": "Q53",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 138,
    "lat1": 68,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/Q54.zip",
    "name": "Q54",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 144,
    "lat1": 68,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/Q55.zip",
    "name": "Q55",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 150,
    "lat1": 68,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/Q56.zip",
    "name": "Q56",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 156,
    "lat1": 68,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/Q57.zip",
    "name": "Q57",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 162,
    "lat1": 68,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/Q58.zip",
    "name": "Q58",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 168,
    "lat1": 68,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/Q59.zip",
    "name": "Q59",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": 174,
    "lat1": 68,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/Q60.zip",
    "name": "Q60",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -180,
    "lat1": 68,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/Q01.zip",
    "name": "Q01",
    "area": 24
  },
  {
    "lat0": 64,
    "lng0": -174,
    "lat1": 68,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/Q02.zip",
    "name": "Q02",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -168,
    "lat1": 64,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/P03.zip",
    "name": "P03",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -162,
    "lat1": 64,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/P04.zip",
    "name": "P04",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -156,
    "lat1": 64,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/P05.zip",
    "name": "P05",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -150,
    "lat1": 64,
    "lng1": -144,
    "uri": "http://viewfinderpanoramas.org/dem3/P06.zip",
    "name": "P06",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -144,
    "lat1": 64,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/P07.zip",
    "name": "P07",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -138,
    "lat1": 64,
    "lng1": -132,
    "uri": "http://viewfinderpanoramas.org/dem3/P08.zip",
    "name": "P08",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -132,
    "lat1": 64,
    "lng1": -126,
    "uri": "http://viewfinderpanoramas.org/dem3/P09.zip",
    "name": "P09",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -126,
    "lat1": 64,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/P10.zip",
    "name": "P10",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -120,
    "lat1": 64,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/P11.zip",
    "name": "P11",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -114,
    "lat1": 64,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/P12.zip",
    "name": "P12",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -108,
    "lat1": 64,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/P13.zip",
    "name": "P13",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -102,
    "lat1": 64,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/P14.zip",
    "name": "P14",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -96,
    "lat1": 64,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/P15.zip",
    "name": "P15",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -90,
    "lat1": 64,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/P16.zip",
    "name": "P16",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -84,
    "lat1": 64,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/P17.zip",
    "name": "P17",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -78,
    "lat1": 64,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/P18.zip",
    "name": "P18",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -72,
    "lat1": 64,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/P19.zip",
    "name": "P19",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -66,
    "lat1": 64,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/P20.zip",
    "name": "P20",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 0,
    "lat1": 64,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/P31v2.zip",
    "name": "P31",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 6,
    "lat1": 64,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/P32v2.zip",
    "name": "P32",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 12,
    "lat1": 64,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/P33v2.zip",
    "name": "P33",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 18,
    "lat1": 64,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/P34v2.zip",
    "name": "P34",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 24,
    "lat1": 64,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/P35v2.zip",
    "name": "P35",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 30,
    "lat1": 64,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/P36v2.zip",
    "name": "P36",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 36,
    "lat1": 64,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/P37v2.zip",
    "name": "P37",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 42,
    "lat1": 64,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/P38v2.zip",
    "name": "P38",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 48,
    "lat1": 64,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/P39v2.zip",
    "name": "P39",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 54,
    "lat1": 64,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/P40v2.zip",
    "name": "P40",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 60,
    "lat1": 64,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/P41.zip",
    "name": "P41",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 66,
    "lat1": 64,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/P42.zip",
    "name": "P42",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 72,
    "lat1": 64,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/P43.zip",
    "name": "P43",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 78,
    "lat1": 64,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/P44.zip",
    "name": "P44",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 84,
    "lat1": 64,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/P45.zip",
    "name": "P45",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 90,
    "lat1": 64,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/P46.zip",
    "name": "P46",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 96,
    "lat1": 64,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/P47.zip",
    "name": "P47",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 102,
    "lat1": 64,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/P48.zip",
    "name": "P48",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 108,
    "lat1": 64,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/P49.zip",
    "name": "P49",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 114,
    "lat1": 64,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/P50.zip",
    "name": "P50",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 120,
    "lat1": 64,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/P51.zip",
    "name": "P51",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 126,
    "lat1": 64,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/P52.zip",
    "name": "P52",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 132,
    "lat1": 64,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/P53.zip",
    "name": "P53",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 138,
    "lat1": 64,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/P54.zip",
    "name": "P54",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 144,
    "lat1": 64,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/P55.zip",
    "name": "P55",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 150,
    "lat1": 64,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/P56.zip",
    "name": "P56",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 156,
    "lat1": 64,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/P57.zip",
    "name": "P57",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 162,
    "lat1": 64,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/P58.zip",
    "name": "P58",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 168,
    "lat1": 64,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/P59.zip",
    "name": "P59",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": 174,
    "lat1": 64,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/P60.zip",
    "name": "P60",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -174,
    "lat1": 64,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/P02.zip",
    "name": "P02",
    "area": 24
  },
  {
    "lat0": 63,
    "lng0": -25,
    "lat1": 67,
    "lng1": -13,
    "uri": "http://viewfinderpanoramas.org/dem3/ISL.zip",
    "name": "ISL",
    "area": 48
  },
  {
    "lat0": 60,
    "lng0": -12,
    "lat1": 64,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/FAR.zip",
    "name": "P29",
    "area": 24
  },
  {
    "lat0": 60,
    "lng0": -6,
    "lat1": 64,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/SHL.zip",
    "name": "P30",
    "area": 24
  },
  {
    "lat0": 68,
    "lng0": -12,
    "lat1": 72,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/JANMAYEN.zip",
    "name": "R29",
    "area": 24
  },
  {
    "lat0": 72,
    "lng0": 18,
    "lat1": 76,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/BEAR.zip",
    "name": "S34",
    "area": 24
  },
  {
    "lat0": 76,
    "lng0": -73,
    "lat1": 84,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/GL-North.zip",
    "name": "GL-N",
    "area": 488
  },
  {
    "lat0": 64,
    "lng0": -60,
    "lat1": 76,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/GL-West.zip",
    "name": "GL-W",
    "area": 216
  },
  {
    "lat0": 64,
    "lng0": -42,
    "lat1": 76,
    "lng1": -17,
    "uri": "http://viewfinderpanoramas.org/dem3/GL-East.zip",
    "name": "GL-E",
    "area": 300
  },
  {
    "lat0": 59,
    "lng0": -52,
    "lat1": 64,
    "lng1": -40,
    "uri": "http://viewfinderpanoramas.org/dem3/GL-South.zip",
    "name": "GL-S",
    "area": 60
  },
  {
    "lat0": 56,
    "lng0": -174,
    "lat1": 60,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/O02.zip",
    "name": "O02",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -168,
    "lat1": 60,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/O03.zip",
    "name": "O03",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -162,
    "lat1": 60,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/O04.zip",
    "name": "O04",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -156,
    "lat1": 60,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/O05.zip",
    "name": "O05",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -150,
    "lat1": 60,
    "lng1": -144,
    "uri": "http://viewfinderpanoramas.org/dem3/O06.zip",
    "name": "O06",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -144,
    "lat1": 60,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/O07.zip",
    "name": "O07",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -138,
    "lat1": 60,
    "lng1": -132,
    "uri": "http://viewfinderpanoramas.org/dem3/O08.zip",
    "name": "O08",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -132,
    "lat1": 60,
    "lng1": -126,
    "uri": "http://viewfinderpanoramas.org/dem3/O09.zip",
    "name": "O09",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -126,
    "lat1": 60,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/O10.zip",
    "name": "O10",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -120,
    "lat1": 60,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/O11.zip",
    "name": "O11",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -114,
    "lat1": 60,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/O12.zip",
    "name": "O12",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -108,
    "lat1": 60,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/O13.zip",
    "name": "O13",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -102,
    "lat1": 60,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/O14.zip",
    "name": "O14",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -96,
    "lat1": 60,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/O15.zip",
    "name": "O15",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -90,
    "lat1": 60,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/O16.zip",
    "name": "O16",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -84,
    "lat1": 60,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/O17.zip",
    "name": "O17",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -78,
    "lat1": 60,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/O18.zip",
    "name": "O18",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -72,
    "lat1": 60,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/O19.zip",
    "name": "O19",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -66,
    "lat1": 60,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/O20.zip",
    "name": "O20",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -18,
    "lat1": 60,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/O28.zip",
    "name": "O28",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -12,
    "lat1": 60,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/O29.zip",
    "name": "O29",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": -6,
    "lat1": 60,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/O30.zip",
    "name": "O30",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 0,
    "lat1": 60,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/O31.zip",
    "name": "O31",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 6,
    "lat1": 60,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/O32.zip",
    "name": "O32",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 12,
    "lat1": 60,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/O33.zip",
    "name": "O33",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 18,
    "lat1": 60,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/O34.zip",
    "name": "O34",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 24,
    "lat1": 60,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/O35.zip",
    "name": "O35",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 30,
    "lat1": 60,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/O36.zip",
    "name": "O36",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 36,
    "lat1": 60,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/O37.zip",
    "name": "O37",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 42,
    "lat1": 60,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/O38.zip",
    "name": "O38",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 48,
    "lat1": 60,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/O39.zip",
    "name": "O39",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 54,
    "lat1": 60,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/O40.zip",
    "name": "O40",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 60,
    "lat1": 60,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/O41.zip",
    "name": "O41",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 66,
    "lat1": 60,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/O42.zip",
    "name": "O42",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 72,
    "lat1": 60,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/O43.zip",
    "name": "O43",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 78,
    "lat1": 60,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/O44.zip",
    "name": "O44",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 84,
    "lat1": 60,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/O45.zip",
    "name": "O45",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 90,
    "lat1": 60,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/O46.zip",
    "name": "O46",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 96,
    "lat1": 60,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/O47.zip",
    "name": "O47",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 102,
    "lat1": 60,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/O48.zip",
    "name": "O48",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 108,
    "lat1": 60,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/O49.zip",
    "name": "O49",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 114,
    "lat1": 60,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/O50.zip",
    "name": "O50",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 120,
    "lat1": 60,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/O51.zip",
    "name": "O51",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 126,
    "lat1": 60,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/O52.zip",
    "name": "O52",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 132,
    "lat1": 60,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/O53.zip",
    "name": "O53",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 138,
    "lat1": 60,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/O54.zip",
    "name": "O54",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 144,
    "lat1": 60,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/O55.zip",
    "name": "O55",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 150,
    "lat1": 60,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/O56.zip",
    "name": "O56",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 156,
    "lat1": 60,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/O57.zip",
    "name": "O57",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 162,
    "lat1": 60,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/O58.zip",
    "name": "O58",
    "area": 24
  },
  {
    "lat0": 56,
    "lng0": 168,
    "lat1": 60,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/O59.zip",
    "name": "O59",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -180,
    "lat1": 56,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/N01.zip",
    "name": "N01",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -174,
    "lat1": 56,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/N02.zip",
    "name": "N02",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -168,
    "lat1": 56,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/N03.zip",
    "name": "N03",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -162,
    "lat1": 56,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/N04.zip",
    "name": "N04",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -156,
    "lat1": 56,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/N05.zip",
    "name": "N05",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -138,
    "lat1": 56,
    "lng1": -132,
    "uri": "http://viewfinderpanoramas.org/dem3/N08.zip",
    "name": "N08",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -132,
    "lat1": 56,
    "lng1": -126,
    "uri": "http://viewfinderpanoramas.org/dem3/N09.zip",
    "name": "N09",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -126,
    "lat1": 56,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/N10.zip",
    "name": "N10",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -120,
    "lat1": 56,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/N11.zip",
    "name": "N11",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -114,
    "lat1": 56,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/N12.zip",
    "name": "N12",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -108,
    "lat1": 56,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/N13.zip",
    "name": "N13",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -102,
    "lat1": 56,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/N14.zip",
    "name": "N14",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -96,
    "lat1": 56,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/N15.zip",
    "name": "N15",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -90,
    "lat1": 56,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/N16.zip",
    "name": "N16",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -84,
    "lat1": 56,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/N17.zip",
    "name": "N17",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -78,
    "lat1": 56,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/N18.zip",
    "name": "N18",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -72,
    "lat1": 56,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/N19.zip",
    "name": "N19",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -66,
    "lat1": 56,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/N20.zip",
    "name": "N20",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -60,
    "lat1": 56,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/N21.zip",
    "name": "N21",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -12,
    "lat1": 56,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/N29.zip",
    "name": "N29",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": -6,
    "lat1": 56,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/N30.zip",
    "name": "N30",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 0,
    "lat1": 56,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/N31.zip",
    "name": "N31",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 6,
    "lat1": 56,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/N32.zip",
    "name": "N32",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 12,
    "lat1": 56,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/N33.zip",
    "name": "N33",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 18,
    "lat1": 56,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/N34.zip",
    "name": "N34",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 24,
    "lat1": 56,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/N35.zip",
    "name": "N35",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 30,
    "lat1": 56,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/N36.zip",
    "name": "N36",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 36,
    "lat1": 56,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/N37.zip",
    "name": "N37",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 42,
    "lat1": 56,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/N38.zip",
    "name": "N38",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 48,
    "lat1": 56,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/N39.zip",
    "name": "N39",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 54,
    "lat1": 56,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/N40.zip",
    "name": "N40",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 60,
    "lat1": 56,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/N41.zip",
    "name": "N41",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 66,
    "lat1": 56,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/N42.zip",
    "name": "N42",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 72,
    "lat1": 56,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/N43.zip",
    "name": "N43",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 78,
    "lat1": 56,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/N44.zip",
    "name": "N44",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 84,
    "lat1": 56,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/N45.zip",
    "name": "N45",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 90,
    "lat1": 56,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/N46.zip",
    "name": "N46",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 96,
    "lat1": 56,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/N47.zip",
    "name": "N47",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 102,
    "lat1": 56,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/N48.zip",
    "name": "N48",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 108,
    "lat1": 56,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/N49.zip",
    "name": "N49",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 114,
    "lat1": 56,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/N50.zip",
    "name": "N50",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 120,
    "lat1": 56,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/N51.zip",
    "name": "N51",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 126,
    "lat1": 56,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/N52.zip",
    "name": "N52",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 132,
    "lat1": 56,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/N53.zip",
    "name": "N53",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 138,
    "lat1": 56,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/N54.zip",
    "name": "N54",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 150,
    "lat1": 56,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/N56.zip",
    "name": "N56",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 156,
    "lat1": 56,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/N57.zip",
    "name": "N57",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 162,
    "lat1": 56,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/N58.zip",
    "name": "N58",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 168,
    "lat1": 56,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/N59.zip",
    "name": "N59",
    "area": 24
  },
  {
    "lat0": 52,
    "lng0": 174,
    "lat1": 56,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/N60.zip",
    "name": "N60",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -180,
    "lat1": 52,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/M01.zip",
    "name": "M01",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -132,
    "lat1": 52,
    "lng1": -126,
    "uri": "http://viewfinderpanoramas.org/dem3/M09.zip",
    "name": "M09",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -126,
    "lat1": 52,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/M10.zip",
    "name": "M10",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -120,
    "lat1": 52,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/M11.zip",
    "name": "M11",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -114,
    "lat1": 52,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/M12.zip",
    "name": "M12",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -108,
    "lat1": 52,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/M13.zip",
    "name": "M13",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -102,
    "lat1": 52,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/M14.zip",
    "name": "M14",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -96,
    "lat1": 52,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/M15.zip",
    "name": "M15",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -90,
    "lat1": 52,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/M16.zip",
    "name": "M16",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -84,
    "lat1": 52,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/M17.zip",
    "name": "M17",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -78,
    "lat1": 52,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/M18.zip",
    "name": "M18",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -72,
    "lat1": 52,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/M19.zip",
    "name": "M19",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -66,
    "lat1": 52,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/M20.zip",
    "name": "M20",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -60,
    "lat1": 52,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/M21.zip",
    "name": "M21",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -54,
    "lat1": 52,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/M22.zip",
    "name": "M22",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -12,
    "lat1": 52,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/M29.zip",
    "name": "M29",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": -6,
    "lat1": 52,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/M30.zip",
    "name": "M30",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 0,
    "lat1": 52,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/M31.zip",
    "name": "M31",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 6,
    "lat1": 52,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/M32.zip",
    "name": "M32",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 12,
    "lat1": 52,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/M33.zip",
    "name": "M33",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 18,
    "lat1": 52,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/M34.zip",
    "name": "M34",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 24,
    "lat1": 52,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/M35.zip",
    "name": "M35",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 30,
    "lat1": 52,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/M36.zip",
    "name": "M36",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 36,
    "lat1": 52,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/M37.zip",
    "name": "M37",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 42,
    "lat1": 52,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/M38.zip",
    "name": "M38",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 48,
    "lat1": 52,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/M39.zip",
    "name": "M39",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 54,
    "lat1": 52,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/M40.zip",
    "name": "M40",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 60,
    "lat1": 52,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/M41.zip",
    "name": "M41",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 66,
    "lat1": 52,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/M42.zip",
    "name": "M42",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 72,
    "lat1": 52,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/M43.zip",
    "name": "M43",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 78,
    "lat1": 52,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/M44.zip",
    "name": "M44",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 84,
    "lat1": 52,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/M45.zip",
    "name": "M45",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 90,
    "lat1": 52,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/M46.zip",
    "name": "M46",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 96,
    "lat1": 52,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/M47.zip",
    "name": "M47",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 102,
    "lat1": 52,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/M48.zip",
    "name": "M48",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 108,
    "lat1": 52,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/M49.zip",
    "name": "M49",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 114,
    "lat1": 52,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/M50.zip",
    "name": "M50",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 120,
    "lat1": 52,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/M51.zip",
    "name": "M51",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 126,
    "lat1": 52,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/M52.zip",
    "name": "M52",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 132,
    "lat1": 52,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/M53.zip",
    "name": "M53",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 138,
    "lat1": 52,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/M54.zip",
    "name": "M54",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 144,
    "lat1": 52,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/M55.zip",
    "name": "M55",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 150,
    "lat1": 52,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/M56.zip",
    "name": "M56",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 156,
    "lat1": 52,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/M57.zip",
    "name": "M57",
    "area": 24
  },
  {
    "lat0": 48,
    "lng0": 174,
    "lat1": 52,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/M60.zip",
    "name": "M60",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -126,
    "lat1": 48,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/L10.zip",
    "name": "L10",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -120,
    "lat1": 48,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/L11.zip",
    "name": "L11",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -114,
    "lat1": 48,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/L12.zip",
    "name": "L12",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -108,
    "lat1": 48,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/L13.zip",
    "name": "L13",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -102,
    "lat1": 48,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/L14.zip",
    "name": "L14",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -96,
    "lat1": 48,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/L15.zip",
    "name": "L15",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -90,
    "lat1": 48,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/L16.zip",
    "name": "L16",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -84,
    "lat1": 48,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/L17.zip",
    "name": "L17",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -78,
    "lat1": 48,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/L18.zip",
    "name": "L18",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -72,
    "lat1": 48,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/L19.zip",
    "name": "L19",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -66,
    "lat1": 48,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/L20.zip",
    "name": "L20",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -60,
    "lat1": 48,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/L21.zip",
    "name": "L21",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -54,
    "lat1": 48,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/L22.zip",
    "name": "L22",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": -6,
    "lat1": 48,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/L30.zip",
    "name": "L30",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 0,
    "lat1": 48,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/L31.zip",
    "name": "L31",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 6,
    "lat1": 48,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/L32.zip",
    "name": "L32",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 12,
    "lat1": 48,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/L33.zip",
    "name": "L33",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 18,
    "lat1": 48,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/L34.zip",
    "name": "L34",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 24,
    "lat1": 48,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/L35.zip",
    "name": "L35",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 30,
    "lat1": 48,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/L36.zip",
    "name": "L36",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 36,
    "lat1": 48,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/L37.zip",
    "name": "L37",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 42,
    "lat1": 48,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/L38.zip",
    "name": "L38",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 48,
    "lat1": 48,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/L39.zip",
    "name": "L39",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 54,
    "lat1": 48,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/L40.zip",
    "name": "L40",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 60,
    "lat1": 48,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/L41.zip",
    "name": "L41",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 66,
    "lat1": 48,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/L42.zip",
    "name": "L42",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 72,
    "lat1": 48,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/L43.zip",
    "name": "L43",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 78,
    "lat1": 48,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/L44.zip",
    "name": "L44",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 84,
    "lat1": 48,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/L45.zip",
    "name": "L45",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 90,
    "lat1": 48,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/L46.zip",
    "name": "L46",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 96,
    "lat1": 48,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/L47.zip",
    "name": "L47",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 102,
    "lat1": 48,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/L48.zip",
    "name": "L48",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 108,
    "lat1": 48,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/L49.zip",
    "name": "L49",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 114,
    "lat1": 48,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/L50.zip",
    "name": "L50",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 120,
    "lat1": 48,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/L51.zip",
    "name": "L51",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 126,
    "lat1": 48,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/L52.zip",
    "name": "L52",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 132,
    "lat1": 48,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/L53.zip",
    "name": "L53",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 138,
    "lat1": 48,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/L54.zip",
    "name": "L54",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 144,
    "lat1": 48,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/L55.zip",
    "name": "L55",
    "area": 24
  },
  {
    "lat0": 44,
    "lng0": 150,
    "lat1": 48,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/L56.zip",
    "name": "L56",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -126,
    "lat1": 44,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/K10.zip",
    "name": "K10",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -120,
    "lat1": 44,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/K11.zip",
    "name": "K11",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -114,
    "lat1": 44,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/K12.zip",
    "name": "K12",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -108,
    "lat1": 44,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/K13.zip",
    "name": "K13",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -102,
    "lat1": 44,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/K14.zip",
    "name": "K14",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -96,
    "lat1": 44,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/K15.zip",
    "name": "K15",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -90,
    "lat1": 44,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/K16.zip",
    "name": "K16",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -84,
    "lat1": 44,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/K17.zip",
    "name": "K17",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -78,
    "lat1": 44,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/K18.zip",
    "name": "K18",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -72,
    "lat1": 44,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/K19.zip",
    "name": "K19",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -66,
    "lat1": 44,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/K20.zip",
    "name": "K20",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -60,
    "lat1": 44,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/K21.zip",
    "name": "K21",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -12,
    "lat1": 44,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/K29.zip",
    "name": "K29",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": -6,
    "lat1": 44,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/K30.zip",
    "name": "K30",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 0,
    "lat1": 44,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/K31.zip",
    "name": "K31",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 6,
    "lat1": 44,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/K32.zip",
    "name": "K32",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 12,
    "lat1": 44,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/K33.zip",
    "name": "K33",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 18,
    "lat1": 44,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/K34.zip",
    "name": "K34",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 24,
    "lat1": 44,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/K35.zip",
    "name": "K35",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 30,
    "lat1": 44,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/K36.zip",
    "name": "K36",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 36,
    "lat1": 44,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/K37.zip",
    "name": "K37",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 42,
    "lat1": 44,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/K38.zip",
    "name": "K38",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 48,
    "lat1": 44,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/K39.zip",
    "name": "K39",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 54,
    "lat1": 44,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/K40.zip",
    "name": "K40",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 60,
    "lat1": 44,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/K41.zip",
    "name": "K41",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 66,
    "lat1": 44,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/K42.zip",
    "name": "K42",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 72,
    "lat1": 44,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/K43.zip",
    "name": "K43",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 78,
    "lat1": 44,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/K44.zip",
    "name": "K44",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 84,
    "lat1": 44,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/K45.zip",
    "name": "K45",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 90,
    "lat1": 44,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/K46.zip",
    "name": "K46",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 96,
    "lat1": 44,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/K47.zip",
    "name": "K47",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 102,
    "lat1": 44,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/K48.zip",
    "name": "K48",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 108,
    "lat1": 44,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/K49.zip",
    "name": "K49",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 114,
    "lat1": 44,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/K50.zip",
    "name": "K50",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 120,
    "lat1": 44,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/K51.zip",
    "name": "K51",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 126,
    "lat1": 44,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/K52.zip",
    "name": "K52",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 132,
    "lat1": 44,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/K53.zip",
    "name": "K53",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 138,
    "lat1": 44,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/K54.zip",
    "name": "K54",
    "area": 24
  },
  {
    "lat0": 40,
    "lng0": 144,
    "lat1": 44,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/K55.zip",
    "name": "K55",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -126,
    "lat1": 40,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/J10.zip",
    "name": "J10",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -120,
    "lat1": 40,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/J11.zip",
    "name": "J11",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -114,
    "lat1": 40,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/J12.zip",
    "name": "J12",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -108,
    "lat1": 40,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/J13.zip",
    "name": "J13",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -102,
    "lat1": 40,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/J14.zip",
    "name": "J14",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -96,
    "lat1": 40,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/J15.zip",
    "name": "J15",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -90,
    "lat1": 40,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/J16.zip",
    "name": "J16",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -84,
    "lat1": 40,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/J17.zip",
    "name": "J17",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -78,
    "lat1": 40,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/J18.zip",
    "name": "J18",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -36,
    "lat1": 40,
    "lng1": -30,
    "uri": "http://viewfinderpanoramas.org/dem3/J25.zip",
    "name": "J25",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -30,
    "lat1": 40,
    "lng1": -24,
    "uri": "http://viewfinderpanoramas.org/dem3/J26.zip",
    "name": "J26",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -12,
    "lat1": 40,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/J29.zip",
    "name": "J29",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": -6,
    "lat1": 40,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/J30.zip",
    "name": "J30",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 0,
    "lat1": 40,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/J31.zip",
    "name": "J31",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 6,
    "lat1": 40,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/J32.zip",
    "name": "J32",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 12,
    "lat1": 40,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/J33.zip",
    "name": "J33",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 18,
    "lat1": 40,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/J34.zip",
    "name": "J34",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 24,
    "lat1": 40,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/J35.zip",
    "name": "J35",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 30,
    "lat1": 40,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/J36.zip",
    "name": "J36",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 36,
    "lat1": 40,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/J37.zip",
    "name": "J37",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 42,
    "lat1": 40,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/J38.zip",
    "name": "J38",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 48,
    "lat1": 40,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/J39.zip",
    "name": "J39",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 54,
    "lat1": 40,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/J40.zip",
    "name": "J40",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 60,
    "lat1": 40,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/J41.zip",
    "name": "J41",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 66,
    "lat1": 40,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/J42.zip",
    "name": "J42",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 72,
    "lat1": 40,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/J43.zip",
    "name": "J43",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 78,
    "lat1": 40,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/J44.zip",
    "name": "J44",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 84,
    "lat1": 40,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/J45.zip",
    "name": "J45",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 90,
    "lat1": 40,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/J46.zip",
    "name": "J46",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 96,
    "lat1": 40,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/J47.zip",
    "name": "J47",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 102,
    "lat1": 40,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/J48.zip",
    "name": "J48",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 108,
    "lat1": 40,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/J49.zip",
    "name": "J49",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 114,
    "lat1": 40,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/J50.zip",
    "name": "J50",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 120,
    "lat1": 40,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/J51.zip",
    "name": "J51",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 126,
    "lat1": 40,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/J52.zip",
    "name": "J52",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 132,
    "lat1": 40,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/J53.zip",
    "name": "J53",
    "area": 24
  },
  {
    "lat0": 36,
    "lng0": 138,
    "lat1": 40,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/J54.zip",
    "name": "J54",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -126,
    "lat1": 36,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/I10.zip",
    "name": "I10",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -120,
    "lat1": 36,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/I11.zip",
    "name": "I11",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -114,
    "lat1": 36,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/I12.zip",
    "name": "I12",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -108,
    "lat1": 36,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/I13.zip",
    "name": "I13",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -102,
    "lat1": 36,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/I14.zip",
    "name": "I14",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -96,
    "lat1": 36,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/I15.zip",
    "name": "I15",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -90,
    "lat1": 36,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/I16.zip",
    "name": "I16",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -84,
    "lat1": 36,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/I17.zip",
    "name": "I17",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -78,
    "lat1": 36,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/I18.zip",
    "name": "I18",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -66,
    "lat1": 36,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/I20.zip",
    "name": "I20",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -18,
    "lat1": 36,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/I28.zip",
    "name": "I28",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -12,
    "lat1": 36,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/I29.zip",
    "name": "I29",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": -6,
    "lat1": 36,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/I30.zip",
    "name": "I30",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 0,
    "lat1": 36,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/I31.zip",
    "name": "I31",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 6,
    "lat1": 36,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/I32.zip",
    "name": "I32",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 12,
    "lat1": 36,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/I33.zip",
    "name": "I33",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 18,
    "lat1": 36,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/I34.zip",
    "name": "I34",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 24,
    "lat1": 36,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/I35.zip",
    "name": "I35",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 30,
    "lat1": 36,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/I36.zip",
    "name": "I36",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 36,
    "lat1": 36,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/I37.zip",
    "name": "I37",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 42,
    "lat1": 36,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/I38.zip",
    "name": "I38",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 48,
    "lat1": 36,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/I39.zip",
    "name": "I39",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 54,
    "lat1": 36,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/I40.zip",
    "name": "I40",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 60,
    "lat1": 36,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/I41.zip",
    "name": "I41",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 66,
    "lat1": 36,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/I42.zip",
    "name": "I42",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 72,
    "lat1": 36,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/I43.zip",
    "name": "I43",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 78,
    "lat1": 36,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/I44.zip",
    "name": "I44",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 84,
    "lat1": 36,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/I45.zip",
    "name": "I45",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 90,
    "lat1": 36,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/I46.zip",
    "name": "I46",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 96,
    "lat1": 36,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/I47.zip",
    "name": "I47",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 102,
    "lat1": 36,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/I48.zip",
    "name": "I48",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 108,
    "lat1": 36,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/I49.zip",
    "name": "I49",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 114,
    "lat1": 36,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/I50.zip",
    "name": "I50",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 120,
    "lat1": 36,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/I51.zip",
    "name": "I51",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 126,
    "lat1": 36,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/I52.zip",
    "name": "I52",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 132,
    "lat1": 36,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/I53.zip",
    "name": "I53",
    "area": 24
  },
  {
    "lat0": 32,
    "lng0": 138,
    "lat1": 36,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/I54.zip",
    "name": "I54",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -180,
    "lat1": 32,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/H01.zip",
    "name": "H01",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -120,
    "lat1": 32,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/H11.zip",
    "name": "H11",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -114,
    "lat1": 32,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/H12.zip",
    "name": "H12",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -108,
    "lat1": 32,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/H13.zip",
    "name": "H13",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -102,
    "lat1": 32,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/H14.zip",
    "name": "H14",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -96,
    "lat1": 32,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/H15.zip",
    "name": "H15",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -90,
    "lat1": 32,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/H16.zip",
    "name": "H16",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -84,
    "lat1": 32,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/H17.zip",
    "name": "H17",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -24,
    "lat1": 32,
    "lng1": -18,
    "uri": "http://viewfinderpanoramas.org/dem3/H27.zip",
    "name": "H27",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -18,
    "lat1": 32,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/H28.zip",
    "name": "H28",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -12,
    "lat1": 32,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/H29.zip",
    "name": "H29",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": -6,
    "lat1": 32,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/H30.zip",
    "name": "H30",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 0,
    "lat1": 32,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/H31.zip",
    "name": "H31",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 6,
    "lat1": 32,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/H32.zip",
    "name": "H32",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 12,
    "lat1": 32,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/H33.zip",
    "name": "H33",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 18,
    "lat1": 32,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/H34.zip",
    "name": "H34",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 24,
    "lat1": 32,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/H35.zip",
    "name": "H35",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 30,
    "lat1": 32,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/H36.zip",
    "name": "H36",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 36,
    "lat1": 32,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/H37.zip",
    "name": "H37",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 42,
    "lat1": 32,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/H38.zip",
    "name": "H38",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 48,
    "lat1": 32,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/H39.zip",
    "name": "H39",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 54,
    "lat1": 32,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/H40.zip",
    "name": "H40",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 60,
    "lat1": 32,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/H41.zip",
    "name": "H41",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 66,
    "lat1": 32,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/H42.zip",
    "name": "H42",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 72,
    "lat1": 32,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/H43.zip",
    "name": "H43",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 78,
    "lat1": 32,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/H44.zip",
    "name": "H44",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 84,
    "lat1": 32,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/H45.zip",
    "name": "H45",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 90,
    "lat1": 32,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/H46.zip",
    "name": "H46",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 96,
    "lat1": 32,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/H47.zip",
    "name": "H47",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 102,
    "lat1": 32,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/H48.zip",
    "name": "H48",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 108,
    "lat1": 32,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/H49.zip",
    "name": "H49",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 114,
    "lat1": 32,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/H50.zip",
    "name": "H50",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 120,
    "lat1": 32,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/H51.zip",
    "name": "H51",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 126,
    "lat1": 32,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/H52.zip",
    "name": "H52",
    "area": 24
  },
  {
    "lat0": 28,
    "lng0": 138,
    "lat1": 32,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/H54.zip",
    "name": "H54",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -180,
    "lat1": 28,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/G01.zip",
    "name": "G01",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -174,
    "lat1": 28,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/G02.zip",
    "name": "G02",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -120,
    "lat1": 28,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/G11.zip",
    "name": "G11",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -114,
    "lat1": 28,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/G12.zip",
    "name": "G12",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -108,
    "lat1": 28,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/G13.zip",
    "name": "G13",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -102,
    "lat1": 28,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/G14.zip",
    "name": "G14",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -84,
    "lat1": 28,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/G17.zip",
    "name": "G17",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -78,
    "lat1": 28,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/G18.zip",
    "name": "G18",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -24,
    "lat1": 28,
    "lng1": -18,
    "uri": "http://viewfinderpanoramas.org/dem3/G27.zip",
    "name": "G27",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -18,
    "lat1": 28,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/G28.zip",
    "name": "G28",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -12,
    "lat1": 28,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/G29.zip",
    "name": "G29",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": -6,
    "lat1": 28,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/G30.zip",
    "name": "G30",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 0,
    "lat1": 28,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/G31.zip",
    "name": "G31",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 6,
    "lat1": 28,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/G32.zip",
    "name": "G32",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 12,
    "lat1": 28,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/G33.zip",
    "name": "G33",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 18,
    "lat1": 28,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/G34.zip",
    "name": "G34",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 24,
    "lat1": 28,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/G35.zip",
    "name": "G35",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 30,
    "lat1": 28,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/G36.zip",
    "name": "G36",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 36,
    "lat1": 28,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/G37.zip",
    "name": "G37",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 42,
    "lat1": 28,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/G38.zip",
    "name": "G38",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 48,
    "lat1": 28,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/G39.zip",
    "name": "G39",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 54,
    "lat1": 28,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/G40.zip",
    "name": "G40",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 60,
    "lat1": 28,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/G41.zip",
    "name": "G41",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 66,
    "lat1": 28,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/G42.zip",
    "name": "G42",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 72,
    "lat1": 28,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/G43.zip",
    "name": "G43",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 78,
    "lat1": 28,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/G44.zip",
    "name": "G44",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 84,
    "lat1": 28,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/G45.zip",
    "name": "G45",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 90,
    "lat1": 28,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/G46.zip",
    "name": "G46",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 96,
    "lat1": 28,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/G47.zip",
    "name": "G47",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 102,
    "lat1": 28,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/G48.zip",
    "name": "G48",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 108,
    "lat1": 28,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/G49.zip",
    "name": "G49",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 114,
    "lat1": 28,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/G50.zip",
    "name": "G50",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 120,
    "lat1": 28,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/G51.zip",
    "name": "G51",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 126,
    "lat1": 28,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/G52.zip",
    "name": "G52",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 138,
    "lat1": 28,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/G54.zip",
    "name": "G54",
    "area": 24
  },
  {
    "lat0": 24,
    "lng0": 150,
    "lat1": 28,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/G56.zip",
    "name": "G56",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -168,
    "lat1": 24,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/F03.zip",
    "name": "F03",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -162,
    "lat1": 24,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/F04.zip",
    "name": "F04",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -156,
    "lat1": 24,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/F05.zip",
    "name": "F05",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -114,
    "lat1": 24,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/F12.zip",
    "name": "F12",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -108,
    "lat1": 24,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/F13.zip",
    "name": "F13",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -102,
    "lat1": 24,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/F14.zip",
    "name": "F14",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -96,
    "lat1": 24,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/F15.zip",
    "name": "F15",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -90,
    "lat1": 24,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/F16.zip",
    "name": "F16",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -84,
    "lat1": 24,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/F17.zip",
    "name": "F17",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -78,
    "lat1": 24,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/F18.zip",
    "name": "F18",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -72,
    "lat1": 24,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/F19.zip",
    "name": "F19",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -18,
    "lat1": 24,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/F28.zip",
    "name": "F28",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -12,
    "lat1": 24,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/F29.zip",
    "name": "F29",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": -6,
    "lat1": 24,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/F30.zip",
    "name": "F30",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 0,
    "lat1": 24,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/F31.zip",
    "name": "F31",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 6,
    "lat1": 24,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/F32.zip",
    "name": "F32",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 12,
    "lat1": 24,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/F33.zip",
    "name": "F33",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 18,
    "lat1": 24,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/F34.zip",
    "name": "F34",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 24,
    "lat1": 24,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/F35.zip",
    "name": "F35",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 30,
    "lat1": 24,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/F36.zip",
    "name": "F36",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 36,
    "lat1": 24,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/F37.zip",
    "name": "F37",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 42,
    "lat1": 24,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/F38.zip",
    "name": "F38",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 48,
    "lat1": 24,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/F39.zip",
    "name": "F39",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 54,
    "lat1": 24,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/F40.zip",
    "name": "F40",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 66,
    "lat1": 24,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/F42.zip",
    "name": "F42",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 72,
    "lat1": 24,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/F43.zip",
    "name": "F43",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 78,
    "lat1": 24,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/F44.zip",
    "name": "F44",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 84,
    "lat1": 24,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/F45.zip",
    "name": "F45",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 90,
    "lat1": 24,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/F46.zip",
    "name": "F46",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 96,
    "lat1": 24,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/F47.zip",
    "name": "F47",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 102,
    "lat1": 24,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/F48.zip",
    "name": "F48",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 108,
    "lat1": 24,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/F49.zip",
    "name": "F49",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 114,
    "lat1": 24,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/F50.zip",
    "name": "F50",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 120,
    "lat1": 24,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/F51.zip",
    "name": "F51",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 132,
    "lat1": 24,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/F53.zip",
    "name": "F53",
    "area": 24
  },
  {
    "lat0": 20,
    "lng0": 144,
    "lat1": 24,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/F55.zip",
    "name": "F55",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -174,
    "lat1": 20,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/E02.zip",
    "name": "E02",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -162,
    "lat1": 20,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/E04.zip",
    "name": "E04",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -156,
    "lat1": 20,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/E05.zip",
    "name": "E05",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -120,
    "lat1": 20,
    "lng1": -114,
    "uri": "http://viewfinderpanoramas.org/dem3/E11.zip",
    "name": "E11",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -114,
    "lat1": 20,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/E12.zip",
    "name": "E12",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -108,
    "lat1": 20,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/E13.zip",
    "name": "E13",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -102,
    "lat1": 20,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/E14.zip",
    "name": "E14",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -96,
    "lat1": 20,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/E15.zip",
    "name": "E15",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -90,
    "lat1": 20,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/E16.zip",
    "name": "E16",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -84,
    "lat1": 20,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/E17.zip",
    "name": "E17",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -78,
    "lat1": 20,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/E18.zip",
    "name": "E18",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -72,
    "lat1": 20,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/E19.zip",
    "name": "E19",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -66,
    "lat1": 20,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/E20.zip",
    "name": "E20",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -30,
    "lat1": 20,
    "lng1": -24,
    "uri": "http://viewfinderpanoramas.org/dem3/E26.zip",
    "name": "E26",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -24,
    "lat1": 20,
    "lng1": -18,
    "uri": "http://viewfinderpanoramas.org/dem3/E27.zip",
    "name": "E27",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -18,
    "lat1": 20,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/E28.zip",
    "name": "E28",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -12,
    "lat1": 20,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/E29.zip",
    "name": "E29",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": -6,
    "lat1": 20,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/E30.zip",
    "name": "E30",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 0,
    "lat1": 20,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/E31.zip",
    "name": "E31",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 6,
    "lat1": 20,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/E32.zip",
    "name": "E32",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 12,
    "lat1": 20,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/E33.zip",
    "name": "E33",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 18,
    "lat1": 20,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/E34.zip",
    "name": "E34",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 24,
    "lat1": 20,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/E35.zip",
    "name": "E35",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 30,
    "lat1": 20,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/E36.zip",
    "name": "E36",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 36,
    "lat1": 20,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/E37.zip",
    "name": "E37",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 42,
    "lat1": 20,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/E38.zip",
    "name": "E38",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 48,
    "lat1": 20,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/E39.zip",
    "name": "E39",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 54,
    "lat1": 20,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/E40.zip",
    "name": "E40",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 72,
    "lat1": 20,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/E43.zip",
    "name": "E43",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 78,
    "lat1": 20,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/E44.zip",
    "name": "E44",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 84,
    "lat1": 20,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/dem3/E45.zip",
    "name": "E45",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 90,
    "lat1": 20,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/E46.zip",
    "name": "E46",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 96,
    "lat1": 20,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/E47.zip",
    "name": "E47",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 102,
    "lat1": 20,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/E48.zip",
    "name": "E48",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 108,
    "lat1": 20,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/E49.zip",
    "name": "E49",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 114,
    "lat1": 20,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/E50.zip",
    "name": "E50",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 120,
    "lat1": 20,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/E51.zip",
    "name": "E51",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 144,
    "lat1": 20,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/E55.zip",
    "name": "E55",
    "area": 24
  },
  {
    "lat0": 16,
    "lng0": 162,
    "lat1": 20,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/E58.zip",
    "name": "E58",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -102,
    "lat1": 16,
    "lng1": -96,
    "uri": "http://viewfinderpanoramas.org/dem3/D14.zip",
    "name": "D14",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -96,
    "lat1": 16,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/D15.zip",
    "name": "D15",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -90,
    "lat1": 16,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/D16.zip",
    "name": "D16",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -84,
    "lat1": 16,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/D17.zip",
    "name": "D17",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -78,
    "lat1": 16,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/D18.zip",
    "name": "D18",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -72,
    "lat1": 16,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/D19.zip",
    "name": "D19",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -66,
    "lat1": 16,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/D20.zip",
    "name": "D20",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -60,
    "lat1": 16,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/D21.zip",
    "name": "D21",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -30,
    "lat1": 16,
    "lng1": -24,
    "uri": "http://viewfinderpanoramas.org/dem3/D26.zip",
    "name": "D26",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -24,
    "lat1": 16,
    "lng1": -18,
    "uri": "http://viewfinderpanoramas.org/dem3/D27.zip",
    "name": "D27",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -18,
    "lat1": 16,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/D28.zip",
    "name": "D28",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -12,
    "lat1": 16,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/D29.zip",
    "name": "D29",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": -6,
    "lat1": 16,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/D30.zip",
    "name": "D30",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 0,
    "lat1": 16,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/D31.zip",
    "name": "D31",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 6,
    "lat1": 16,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/D32.zip",
    "name": "D32",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 12,
    "lat1": 16,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/D33.zip",
    "name": "D33",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 18,
    "lat1": 16,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/D34.zip",
    "name": "D34",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 24,
    "lat1": 16,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/D35.zip",
    "name": "D35",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 30,
    "lat1": 16,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/D36.zip",
    "name": "D36",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 36,
    "lat1": 16,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/D37.zip",
    "name": "D37",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 42,
    "lat1": 16,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/D38.zip",
    "name": "D38",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 48,
    "lat1": 16,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/D39.zip",
    "name": "D39",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 54,
    "lat1": 16,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/D40.zip",
    "name": "D40",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 72,
    "lat1": 16,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/D43.zip",
    "name": "D43",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 78,
    "lat1": 16,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/D44.zip",
    "name": "D44",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 90,
    "lat1": 16,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/D46.zip",
    "name": "D46",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 96,
    "lat1": 16,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/D47.zip",
    "name": "D47",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 102,
    "lat1": 16,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/D48.zip",
    "name": "D48",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 108,
    "lat1": 16,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/D49.zip",
    "name": "D49",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 114,
    "lat1": 16,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/D50.zip",
    "name": "D50",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 120,
    "lat1": 16,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/D51.zip",
    "name": "D51",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 144,
    "lat1": 16,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/D55.zip",
    "name": "D55",
    "area": 24
  },
  {
    "lat0": 12,
    "lng0": 168,
    "lat1": 16,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/D59.zip",
    "name": "D59",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -114,
    "lat1": 12,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/C12.zip",
    "name": "C12",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -90,
    "lat1": 12,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/C16.zip",
    "name": "C16",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -84,
    "lat1": 12,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/C17.zip",
    "name": "C17",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -78,
    "lat1": 12,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/C18.zip",
    "name": "C18",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -72,
    "lat1": 12,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/C19.zip",
    "name": "C19",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -66,
    "lat1": 12,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/C20.zip",
    "name": "C20",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -60,
    "lat1": 12,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/C21.zip",
    "name": "C21",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -18,
    "lat1": 12,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/C28.zip",
    "name": "C28",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -12,
    "lat1": 12,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/C29.zip",
    "name": "C29",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": -6,
    "lat1": 12,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/C30.zip",
    "name": "C30",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 0,
    "lat1": 12,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/C31.zip",
    "name": "C31",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 6,
    "lat1": 12,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/C32.zip",
    "name": "C32",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 12,
    "lat1": 12,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/C33.zip",
    "name": "C33",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 18,
    "lat1": 12,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/C34.zip",
    "name": "C34",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 24,
    "lat1": 12,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/C35.zip",
    "name": "C35",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 30,
    "lat1": 12,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/C36.zip",
    "name": "C36",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 36,
    "lat1": 12,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/C37.zip",
    "name": "C37",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 42,
    "lat1": 12,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/C38.zip",
    "name": "C38",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 48,
    "lat1": 12,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/C39.zip",
    "name": "C39",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 72,
    "lat1": 12,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/C43.zip",
    "name": "C43",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 78,
    "lat1": 12,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/C44.zip",
    "name": "C44",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 90,
    "lat1": 12,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/C46.zip",
    "name": "C46",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 96,
    "lat1": 12,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/C47.zip",
    "name": "C47",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 102,
    "lat1": 12,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/C48.zip",
    "name": "C48",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 108,
    "lat1": 12,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/C49.zip",
    "name": "C49",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 114,
    "lat1": 12,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/C50.zip",
    "name": "C50",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 120,
    "lat1": 12,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/C51.zip",
    "name": "C51",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 126,
    "lat1": 12,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/C52.zip",
    "name": "C52",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 132,
    "lat1": 12,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/C53.zip",
    "name": "C53",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 138,
    "lat1": 12,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/C54.zip",
    "name": "C54",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 144,
    "lat1": 12,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/C55.zip",
    "name": "C55",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 150,
    "lat1": 12,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/C56.zip",
    "name": "C56",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 156,
    "lat1": 12,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/C57.zip",
    "name": "C57",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 162,
    "lat1": 12,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/C58.zip",
    "name": "C58",
    "area": 24
  },
  {
    "lat0": 8,
    "lng0": 168,
    "lat1": 12,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/C59.zip",
    "name": "C59",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -168,
    "lat1": 8,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/B03.zip",
    "name": "B03",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -162,
    "lat1": 8,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/B04.zip",
    "name": "B04",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -90,
    "lat1": 8,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/B16.zip",
    "name": "B16",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -84,
    "lat1": 8,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/B17.zip",
    "name": "B17",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -78,
    "lat1": 8,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/B18.zip",
    "name": "B18",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -72,
    "lat1": 8,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/B19.zip",
    "name": "B19",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -66,
    "lat1": 8,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/B20.zip",
    "name": "B20",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -60,
    "lat1": 8,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/B21.zip",
    "name": "B21",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -54,
    "lat1": 8,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/B22.zip",
    "name": "B22",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -18,
    "lat1": 8,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/B28.zip",
    "name": "B28",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -12,
    "lat1": 8,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/B29.zip",
    "name": "B29",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": -6,
    "lat1": 8,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/B30.zip",
    "name": "B30",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 0,
    "lat1": 8,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/B31.zip",
    "name": "B31",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 6,
    "lat1": 8,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/B32.zip",
    "name": "B32",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 12,
    "lat1": 8,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/B33.zip",
    "name": "B33",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 18,
    "lat1": 8,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/B34.zip",
    "name": "B34",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 24,
    "lat1": 8,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/B35.zip",
    "name": "B35",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 30,
    "lat1": 8,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/B36.zip",
    "name": "B36",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 36,
    "lat1": 8,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/B37.zip",
    "name": "B37",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 42,
    "lat1": 8,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/B38.zip",
    "name": "B38",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 48,
    "lat1": 8,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/B39.zip",
    "name": "B39",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 72,
    "lat1": 8,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/B43.zip",
    "name": "B43",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 78,
    "lat1": 8,
    "lng1": 84,
    "uri": "http://viewfinderpanoramas.org/dem3/B44.zip",
    "name": "B44",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 90,
    "lat1": 8,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/B46.zip",
    "name": "B46",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 96,
    "lat1": 8,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/B47.zip",
    "name": "B47",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 102,
    "lat1": 8,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/B48.zip",
    "name": "B48",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 108,
    "lat1": 8,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/B49.zip",
    "name": "B49",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 114,
    "lat1": 8,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/B50.zip",
    "name": "B50",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 120,
    "lat1": 8,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/B51.zip",
    "name": "B51",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 126,
    "lat1": 8,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/B52.zip",
    "name": "B52",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 132,
    "lat1": 8,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/B53.zip",
    "name": "B53",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 138,
    "lat1": 8,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/B54.zip",
    "name": "B54",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 144,
    "lat1": 8,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/B55.zip",
    "name": "B55",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 150,
    "lat1": 8,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/B56.zip",
    "name": "B56",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 156,
    "lat1": 8,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/B57.zip",
    "name": "B57",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 162,
    "lat1": 8,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/B58.zip",
    "name": "B58",
    "area": 24
  },
  {
    "lat0": 4,
    "lng0": 168,
    "lat1": 8,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/B59.zip",
    "name": "B59",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -180,
    "lat1": 4,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/A01.zip",
    "name": "A01",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -162,
    "lat1": 4,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/A04.zip",
    "name": "A04",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -96,
    "lat1": 4,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/A15.zip",
    "name": "A15",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -90,
    "lat1": 4,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/A16.zip",
    "name": "A16",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -84,
    "lat1": 4,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/A17.zip",
    "name": "A17",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -78,
    "lat1": 4,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/A18.zip",
    "name": "A18",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -72,
    "lat1": 4,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/A19.zip",
    "name": "A19",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -66,
    "lat1": 4,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/A20.zip",
    "name": "A20",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -60,
    "lat1": 4,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/A21.zip",
    "name": "A21",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": -54,
    "lat1": 4,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/A22.zip",
    "name": "A22",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 6,
    "lat1": 4,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/A32.zip",
    "name": "A32",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 12,
    "lat1": 4,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/A33.zip",
    "name": "A33",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 18,
    "lat1": 4,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/A34.zip",
    "name": "A34",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 24,
    "lat1": 4,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/A35.zip",
    "name": "A35",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 30,
    "lat1": 4,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/A36.zip",
    "name": "A36",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 36,
    "lat1": 4,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/A37.zip",
    "name": "A37",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 42,
    "lat1": 4,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/A38.zip",
    "name": "A38",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 72,
    "lat1": 4,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/A43.zip",
    "name": "A43",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 90,
    "lat1": 4,
    "lng1": 96,
    "uri": "http://viewfinderpanoramas.org/dem3/A46.zip",
    "name": "A46",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 96,
    "lat1": 4,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/A47.zip",
    "name": "A47",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 102,
    "lat1": 4,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/A48.zip",
    "name": "A48",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 108,
    "lat1": 4,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/A49.zip",
    "name": "A49",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 114,
    "lat1": 4,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/A50.zip",
    "name": "A50",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 120,
    "lat1": 4,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/A51.zip",
    "name": "A51",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 126,
    "lat1": 4,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/A52.zip",
    "name": "A52",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 132,
    "lat1": 4,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/A53.zip",
    "name": "A53",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 150,
    "lat1": 4,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/A56.zip",
    "name": "A56",
    "area": 24
  },
  {
    "lat0": 0,
    "lng0": 168,
    "lat1": 4,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/A59.zip",
    "name": "A59",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -180,
    "lat1": 0,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/SA01.zip",
    "name": "SA01",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -174,
    "lat1": 0,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/SA02.zip",
    "name": "SA02",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -162,
    "lat1": 0,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/SA04.zip",
    "name": "SA04",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -156,
    "lat1": 0,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/SA05.zip",
    "name": "SA05",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -96,
    "lat1": 0,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/SA15.zip",
    "name": "SA15",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -90,
    "lat1": 0,
    "lng1": -84,
    "uri": "http://viewfinderpanoramas.org/dem3/SA16.zip",
    "name": "SA16",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -84,
    "lat1": 0,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/SA17.zip",
    "name": "SA17",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -78,
    "lat1": 0,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SA18.zip",
    "name": "SA18",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -72,
    "lat1": 0,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SA19.zip",
    "name": "SA19",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -66,
    "lat1": 0,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SA20.zip",
    "name": "SA20",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -60,
    "lat1": 0,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SA21.zip",
    "name": "SA21",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -54,
    "lat1": 0,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SA22.zip",
    "name": "SA22",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -48,
    "lat1": 0,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/SA23.zip",
    "name": "SA23",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -42,
    "lat1": 0,
    "lng1": -36,
    "uri": "http://viewfinderpanoramas.org/dem3/SA24.zip",
    "name": "SA24",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": -36,
    "lat1": 0,
    "lng1": -30,
    "uri": "http://viewfinderpanoramas.org/dem3/SA25.zip",
    "name": "SA25",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 0,
    "lat1": 0,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/SA31.zip",
    "name": "SA31",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 6,
    "lat1": 0,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/SA32.zip",
    "name": "SA32",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 12,
    "lat1": 0,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SA33.zip",
    "name": "SA33",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 18,
    "lat1": 0,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SA34.zip",
    "name": "SA34",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 24,
    "lat1": 0,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SA35.zip",
    "name": "SA35",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 30,
    "lat1": 0,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SA36.zip",
    "name": "SA36",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 36,
    "lat1": 0,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/SA37.zip",
    "name": "SA37",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 42,
    "lat1": 0,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/SA38.zip",
    "name": "SA38",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 54,
    "lat1": 0,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/SA40.zip",
    "name": "SA40",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 72,
    "lat1": 0,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/SA43.zip",
    "name": "SA43",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 96,
    "lat1": 0,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/SA47.zip",
    "name": "SA47",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 102,
    "lat1": 0,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/SA48.zip",
    "name": "SA48",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 108,
    "lat1": 0,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/SA49.zip",
    "name": "SA49",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 114,
    "lat1": 0,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/SA50.zip",
    "name": "SA50",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 120,
    "lat1": 0,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SA51.zip",
    "name": "SA51",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 126,
    "lat1": 0,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SA52.zip",
    "name": "SA52",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 132,
    "lat1": 0,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SA53.zip",
    "name": "SA53",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 138,
    "lat1": 0,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SA54.zip",
    "name": "SA54",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 144,
    "lat1": 0,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SA55.zip",
    "name": "SA55",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 150,
    "lat1": 0,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SA56.zip",
    "name": "SA56",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 162,
    "lat1": 0,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SA58.zip",
    "name": "SA58",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 168,
    "lat1": 0,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SA59.zip",
    "name": "SA59",
    "area": 24
  },
  {
    "lat0": -4,
    "lng0": 174,
    "lat1": 0,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SA60.zip",
    "name": "SA60",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -180,
    "lat1": -4,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/SB01.zip",
    "name": "SB01",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -174,
    "lat1": -4,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/SB02.zip",
    "name": "SB02",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -156,
    "lat1": -4,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/SB05.zip",
    "name": "SB05",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -144,
    "lat1": -4,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/SB07.zip",
    "name": "SB07",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -84,
    "lat1": -4,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/SB17.zip",
    "name": "SB17",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -78,
    "lat1": -4,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SB18.zip",
    "name": "SB18",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -72,
    "lat1": -4,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SB19.zip",
    "name": "SB19",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -66,
    "lat1": -4,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SB20.zip",
    "name": "SB20",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -60,
    "lat1": -4,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SB21.zip",
    "name": "SB21",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -54,
    "lat1": -4,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SB22.zip",
    "name": "SB22",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -48,
    "lat1": -4,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/SB23.zip",
    "name": "SB23",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -42,
    "lat1": -4,
    "lng1": -36,
    "uri": "http://viewfinderpanoramas.org/dem3/SB24.zip",
    "name": "SB24",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -36,
    "lat1": -4,
    "lng1": -30,
    "uri": "http://viewfinderpanoramas.org/dem3/SB25.zip",
    "name": "SB25",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": -18,
    "lat1": -4,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/SB28.zip",
    "name": "SB28",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 6,
    "lat1": -4,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/SB32.zip",
    "name": "SB32",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 12,
    "lat1": -4,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SB33.zip",
    "name": "SB33",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 18,
    "lat1": -4,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SB34.zip",
    "name": "SB34",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 24,
    "lat1": -4,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SB35.zip",
    "name": "SB35",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 30,
    "lat1": -4,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SB36.zip",
    "name": "SB36",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 36,
    "lat1": -4,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/SB37.zip",
    "name": "SB37",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 48,
    "lat1": -4,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/SB39.zip",
    "name": "SB39",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 54,
    "lat1": -4,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/SB40.zip",
    "name": "SB40",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 66,
    "lat1": -4,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/SB42.zip",
    "name": "SB42",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 72,
    "lat1": -4,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/SB43.zip",
    "name": "SB43",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 96,
    "lat1": -4,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/SB47.zip",
    "name": "SB47",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 102,
    "lat1": -4,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/SB48.zip",
    "name": "SB48",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 108,
    "lat1": -4,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/SB49.zip",
    "name": "SB49",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 114,
    "lat1": -4,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/SB50.zip",
    "name": "SB50",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 120,
    "lat1": -4,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SB51.zip",
    "name": "SB51",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 126,
    "lat1": -4,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SB52.zip",
    "name": "SB52",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 132,
    "lat1": -4,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SB53.zip",
    "name": "SB53",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 138,
    "lat1": -4,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SB54.zip",
    "name": "SB54",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 144,
    "lat1": -4,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SB55.zip",
    "name": "SB55",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 150,
    "lat1": -4,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SB56.zip",
    "name": "SB56",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 156,
    "lat1": -4,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/SB57.zip",
    "name": "SB57",
    "area": 24
  },
  {
    "lat0": -8,
    "lng0": 174,
    "lat1": -4,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SB60.zip",
    "name": "SB60",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -174,
    "lat1": -8,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/SC02.zip",
    "name": "SC02",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -168,
    "lat1": -8,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/SC03.zip",
    "name": "SC03",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -162,
    "lat1": -8,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/SC04.zip",
    "name": "SC04",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -156,
    "lat1": -8,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/SC05.zip",
    "name": "SC05",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -144,
    "lat1": -8,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/SC07.zip",
    "name": "SC07",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -84,
    "lat1": -8,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/SC17.zip",
    "name": "SC17",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -78,
    "lat1": -8,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SC18.zip",
    "name": "SC18",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -72,
    "lat1": -8,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SC19.zip",
    "name": "SC19",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -66,
    "lat1": -8,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SC20.zip",
    "name": "SC20",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -60,
    "lat1": -8,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SC21.zip",
    "name": "SC21",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -54,
    "lat1": -8,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SC22.zip",
    "name": "SC22",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -48,
    "lat1": -8,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/SC23.zip",
    "name": "SC23",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -42,
    "lat1": -8,
    "lng1": -36,
    "uri": "http://viewfinderpanoramas.org/dem3/SC24.zip",
    "name": "SC24",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": -36,
    "lat1": -8,
    "lng1": -30,
    "uri": "http://viewfinderpanoramas.org/dem3/SC25.zip",
    "name": "SC25",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 12,
    "lat1": -8,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SC33.zip",
    "name": "SC33",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 18,
    "lat1": -8,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SC34.zip",
    "name": "SC34",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 24,
    "lat1": -8,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SC35.zip",
    "name": "SC35",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 30,
    "lat1": -8,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SC36.zip",
    "name": "SC36",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 36,
    "lat1": -8,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/SC37.zip",
    "name": "SC37",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 42,
    "lat1": -8,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/SC38.zip",
    "name": "SC38",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 48,
    "lat1": -8,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/SC39.zip",
    "name": "SC39",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 54,
    "lat1": -8,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/SC40.zip",
    "name": "SC40",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 96,
    "lat1": -8,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/SC47.zip",
    "name": "SC47",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 102,
    "lat1": -8,
    "lng1": 108,
    "uri": "http://viewfinderpanoramas.org/dem3/SC48.zip",
    "name": "SC48",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 108,
    "lat1": -8,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/SC49.zip",
    "name": "SC49",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 114,
    "lat1": -8,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/SC50.zip",
    "name": "SC50",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 120,
    "lat1": -8,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SC51.zip",
    "name": "SC51",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 126,
    "lat1": -8,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SC52.zip",
    "name": "SC52",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 132,
    "lat1": -8,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SC53.zip",
    "name": "SC53",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 138,
    "lat1": -8,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SC54.zip",
    "name": "SC54",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 144,
    "lat1": -8,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SC55.zip",
    "name": "SC55",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 150,
    "lat1": -8,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SC56.zip",
    "name": "SC56",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 156,
    "lat1": -8,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/SC57.zip",
    "name": "SC57",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 162,
    "lat1": -8,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SC58.zip",
    "name": "SC58",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 168,
    "lat1": -8,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SC59.zip",
    "name": "SC59",
    "area": 24
  },
  {
    "lat0": -12,
    "lng0": 174,
    "lat1": -8,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SC60.zip",
    "name": "SC60",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -180,
    "lat1": -12,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/SD01.zip",
    "name": "SD01",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -174,
    "lat1": -12,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/SD02.zip",
    "name": "SD02",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -168,
    "lat1": -12,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/SD03.zip",
    "name": "SD03",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -156,
    "lat1": -12,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/SD05.zip",
    "name": "SD05",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -150,
    "lat1": -12,
    "lng1": -144,
    "uri": "http://viewfinderpanoramas.org/dem3/SD06.zip",
    "name": "SD06",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -144,
    "lat1": -12,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/SD07.zip",
    "name": "SD07",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -78,
    "lat1": -12,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SD18.zip",
    "name": "SD18",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -72,
    "lat1": -12,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SD19.zip",
    "name": "SD19",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -66,
    "lat1": -12,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SD20.zip",
    "name": "SD20",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -60,
    "lat1": -12,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SD21.zip",
    "name": "SD21",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -54,
    "lat1": -12,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SD22.zip",
    "name": "SD22",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -48,
    "lat1": -12,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/SD23.zip",
    "name": "SD23",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -42,
    "lat1": -12,
    "lng1": -36,
    "uri": "http://viewfinderpanoramas.org/dem3/SD24.zip",
    "name": "SD24",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": -6,
    "lat1": -12,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/SD30.zip",
    "name": "SD30",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 6,
    "lat1": -12,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/SD32.zip",
    "name": "SD32",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 12,
    "lat1": -12,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SD33.zip",
    "name": "SD33",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 18,
    "lat1": -12,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SD34.zip",
    "name": "SD34",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 24,
    "lat1": -12,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SD35.zip",
    "name": "SD35",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 30,
    "lat1": -12,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SD36.zip",
    "name": "SD36",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 36,
    "lat1": -12,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/SD37.zip",
    "name": "SD37",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 42,
    "lat1": -12,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/SD38.zip",
    "name": "SD38",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 48,
    "lat1": -12,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/SD39.zip",
    "name": "SD39",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 54,
    "lat1": -12,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/SD40.zip",
    "name": "SD40",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 96,
    "lat1": -12,
    "lng1": 102,
    "uri": "http://viewfinderpanoramas.org/dem3/SD47.zip",
    "name": "SD47",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 120,
    "lat1": -12,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SD51.zip",
    "name": "SD51",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 126,
    "lat1": -12,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SD52.zip",
    "name": "SD52",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 132,
    "lat1": -12,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SD53.zip",
    "name": "SD53",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 138,
    "lat1": -12,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SD54.zip",
    "name": "SD54",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 144,
    "lat1": -12,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SD55.zip",
    "name": "SD55",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 162,
    "lat1": -12,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SD58.zip",
    "name": "SD58",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 168,
    "lat1": -12,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SD59.zip",
    "name": "SD59",
    "area": 24
  },
  {
    "lat0": -16,
    "lng0": 174,
    "lat1": -12,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SD60.zip",
    "name": "SD60",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -180,
    "lat1": -16,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/SE01.zip",
    "name": "SE01",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -174,
    "lat1": -16,
    "lng1": -168,
    "uri": "http://viewfinderpanoramas.org/dem3/SE02.zip",
    "name": "SE02",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -168,
    "lat1": -16,
    "lng1": -162,
    "uri": "http://viewfinderpanoramas.org/dem3/SE03.zip",
    "name": "SE03",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -162,
    "lat1": -16,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/SE04.zip",
    "name": "SE04",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -156,
    "lat1": -16,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/SE05.zip",
    "name": "SE05",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -150,
    "lat1": -16,
    "lng1": -144,
    "uri": "http://viewfinderpanoramas.org/dem3/SE06.zip",
    "name": "SE06",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -144,
    "lat1": -16,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/SE07.zip",
    "name": "SE07",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -138,
    "lat1": -16,
    "lng1": -132,
    "uri": "http://viewfinderpanoramas.org/dem3/SE08.zip",
    "name": "SE08",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -78,
    "lat1": -16,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SE18.zip",
    "name": "SE18",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -72,
    "lat1": -16,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SE19.zip",
    "name": "SE19",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -66,
    "lat1": -16,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SE20.zip",
    "name": "SE20",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -60,
    "lat1": -16,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SE21.zip",
    "name": "SE21",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -54,
    "lat1": -16,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SE22.zip",
    "name": "SE22",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -48,
    "lat1": -16,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/SE23.zip",
    "name": "SE23",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -42,
    "lat1": -16,
    "lng1": -36,
    "uri": "http://viewfinderpanoramas.org/dem3/SE24.zip",
    "name": "SE24",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": -6,
    "lat1": -16,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/dem3/SE30.zip",
    "name": "SE30",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 6,
    "lat1": -16,
    "lng1": 12,
    "uri": "http://viewfinderpanoramas.org/dem3/SE32.zip",
    "name": "SE32",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 12,
    "lat1": -16,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SE33.zip",
    "name": "SE33",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 18,
    "lat1": -16,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SE34.zip",
    "name": "SE34",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 24,
    "lat1": -16,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SE35.zip",
    "name": "SE35",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 30,
    "lat1": -16,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SE36.zip",
    "name": "SE36",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 36,
    "lat1": -16,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/SE37.zip",
    "name": "SE37",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 42,
    "lat1": -16,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/SE38.zip",
    "name": "SE38",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 48,
    "lat1": -16,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/SE39.zip",
    "name": "SE39",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 54,
    "lat1": -16,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/SE40.zip",
    "name": "SE40",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 60,
    "lat1": -16,
    "lng1": 66,
    "uri": "http://viewfinderpanoramas.org/dem3/SE41.zip",
    "name": "SE41",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 114,
    "lat1": -16,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/SE50.zip",
    "name": "SE50",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 120,
    "lat1": -16,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SE51.zip",
    "name": "SE51",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 126,
    "lat1": -16,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SE52.zip",
    "name": "SE52",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 132,
    "lat1": -16,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SE53.zip",
    "name": "SE53",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 138,
    "lat1": -16,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SE54.zip",
    "name": "SE54",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 144,
    "lat1": -16,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SE55.zip",
    "name": "SE55",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 150,
    "lat1": -16,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SE56.zip",
    "name": "SE56",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 156,
    "lat1": -16,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/SE57.zip",
    "name": "SE57",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 162,
    "lat1": -16,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SE58.zip",
    "name": "SE58",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 168,
    "lat1": -16,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SE59.zip",
    "name": "SE59",
    "area": 24
  },
  {
    "lat0": -20,
    "lng0": 174,
    "lat1": -16,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SE60.zip",
    "name": "SE60",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -180,
    "lat1": -20,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/SF01.zip",
    "name": "SF01",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -162,
    "lat1": -20,
    "lng1": -156,
    "uri": "http://viewfinderpanoramas.org/dem3/SF04.zip",
    "name": "SF04",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -156,
    "lat1": -20,
    "lng1": -150,
    "uri": "http://viewfinderpanoramas.org/dem3/SF05.zip",
    "name": "SF05",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -150,
    "lat1": -20,
    "lng1": -144,
    "uri": "http://viewfinderpanoramas.org/dem3/SF06.zip",
    "name": "SF06",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -144,
    "lat1": -20,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/SF07.zip",
    "name": "SF07",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -138,
    "lat1": -20,
    "lng1": -132,
    "uri": "http://viewfinderpanoramas.org/dem3/SF08.zip",
    "name": "SF08",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -132,
    "lat1": -20,
    "lng1": -126,
    "uri": "http://viewfinderpanoramas.org/dem3/SF09.zip",
    "name": "SF09",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -72,
    "lat1": -20,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SF19.zip",
    "name": "SF19",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -66,
    "lat1": -20,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SF20.zip",
    "name": "SF20",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -60,
    "lat1": -20,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SF21.zip",
    "name": "SF21",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -54,
    "lat1": -20,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SF22.zip",
    "name": "SF22",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -48,
    "lat1": -20,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/SF23.zip",
    "name": "SF23",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -42,
    "lat1": -20,
    "lng1": -36,
    "uri": "http://viewfinderpanoramas.org/dem3/SF24.zip",
    "name": "SF24",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": -30,
    "lat1": -20,
    "lng1": -24,
    "uri": "http://viewfinderpanoramas.org/dem3/SF26.zip",
    "name": "SF26",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 12,
    "lat1": -20,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SF33.zip",
    "name": "SF33",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 18,
    "lat1": -20,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SF34.zip",
    "name": "SF34",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 24,
    "lat1": -20,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SF35.zip",
    "name": "SF35",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 30,
    "lat1": -20,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SF36.zip",
    "name": "SF36",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 36,
    "lat1": -20,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/SF37.zip",
    "name": "SF37",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 42,
    "lat1": -20,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/SF38.zip",
    "name": "SF38",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 48,
    "lat1": -20,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/SF39.zip",
    "name": "SF39",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 54,
    "lat1": -20,
    "lng1": 60,
    "uri": "http://viewfinderpanoramas.org/dem3/SF40.zip",
    "name": "SF40",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 108,
    "lat1": -20,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/SF49.zip",
    "name": "SF49",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 114,
    "lat1": -20,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/SF50.zip",
    "name": "SF50",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 120,
    "lat1": -20,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SF51.zip",
    "name": "SF51",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 126,
    "lat1": -20,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SF52.zip",
    "name": "SF52",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 132,
    "lat1": -20,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SF53.zip",
    "name": "SF53",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 138,
    "lat1": -20,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SF54.zip",
    "name": "SF54",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 144,
    "lat1": -20,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SF55.zip",
    "name": "SF55",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 150,
    "lat1": -20,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SF56.zip",
    "name": "SF56",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 156,
    "lat1": -20,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/SF57.zip",
    "name": "SF57",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 162,
    "lat1": -20,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SF58.zip",
    "name": "SF58",
    "area": 24
  },
  {
    "lat0": -24,
    "lng0": 168,
    "lat1": -20,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SF59.zip",
    "name": "SF59",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -150,
    "lat1": -24,
    "lng1": -144,
    "uri": "http://viewfinderpanoramas.org/dem3/SG06.zip",
    "name": "SG06",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -144,
    "lat1": -24,
    "lng1": -138,
    "uri": "http://viewfinderpanoramas.org/dem3/SG07.zip",
    "name": "SG07",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -132,
    "lat1": -24,
    "lng1": -126,
    "uri": "http://viewfinderpanoramas.org/dem3/SG09.zip",
    "name": "SG09",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -126,
    "lat1": -24,
    "lng1": -120,
    "uri": "http://viewfinderpanoramas.org/dem3/SG10.zip",
    "name": "SG10",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -114,
    "lat1": -24,
    "lng1": -108,
    "uri": "http://viewfinderpanoramas.org/dem3/SG12.zip",
    "name": "SG12",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -108,
    "lat1": -24,
    "lng1": -102,
    "uri": "http://viewfinderpanoramas.org/dem3/SG13.zip",
    "name": "SG13",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -84,
    "lat1": -24,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/SG17.zip",
    "name": "SG17",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -72,
    "lat1": -24,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SG19.zip",
    "name": "SG19",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -66,
    "lat1": -24,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SG20.zip",
    "name": "SG20",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -60,
    "lat1": -24,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SG21.zip",
    "name": "SG21",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -54,
    "lat1": -24,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SG22.zip",
    "name": "SG22",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": -48,
    "lat1": -24,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/SG23.zip",
    "name": "SG23",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 12,
    "lat1": -24,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SG33.zip",
    "name": "SG33",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 18,
    "lat1": -24,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SG34.zip",
    "name": "SG34",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 24,
    "lat1": -24,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SG35.zip",
    "name": "SG35",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 30,
    "lat1": -24,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SG36.zip",
    "name": "SG36",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 42,
    "lat1": -24,
    "lng1": 48,
    "uri": "http://viewfinderpanoramas.org/dem3/SG38.zip",
    "name": "SG38",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 108,
    "lat1": -24,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/SG49.zip",
    "name": "SG49",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 114,
    "lat1": -24,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/SG50.zip",
    "name": "SG50",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 120,
    "lat1": -24,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SG51.zip",
    "name": "SG51",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 126,
    "lat1": -24,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SG52.zip",
    "name": "SG52",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 132,
    "lat1": -24,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SG53.zip",
    "name": "SG53",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 138,
    "lat1": -24,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SG54.zip",
    "name": "SG54",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 144,
    "lat1": -24,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SG55.zip",
    "name": "SG55",
    "area": 24
  },
  {
    "lat0": -28,
    "lng0": 150,
    "lat1": -24,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SG56.zip",
    "name": "SG56",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": -180,
    "lat1": -28,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/SH01.zip",
    "name": "SH01",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": -72,
    "lat1": -28,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SH19.zip",
    "name": "SH19",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": -66,
    "lat1": -28,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SH20.zip",
    "name": "SH20",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": -60,
    "lat1": -28,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SH21.zip",
    "name": "SH21",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": -54,
    "lat1": -28,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SH22.zip",
    "name": "SH22",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 12,
    "lat1": -28,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SH33.zip",
    "name": "SH33",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 18,
    "lat1": -28,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SH34.zip",
    "name": "SH34",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 24,
    "lat1": -28,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SH35.zip",
    "name": "SH35",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 30,
    "lat1": -28,
    "lng1": 36,
    "uri": "http://viewfinderpanoramas.org/dem3/SH36.zip",
    "name": "SH36",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 108,
    "lat1": -28,
    "lng1": 114,
    "uri": "http://viewfinderpanoramas.org/dem3/SH49.zip",
    "name": "SH49",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 114,
    "lat1": -28,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/SH50.zip",
    "name": "SH50",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 120,
    "lat1": -28,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SH51.zip",
    "name": "SH51",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 126,
    "lat1": -28,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SH52.zip",
    "name": "SH52",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 132,
    "lat1": -28,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SH53.zip",
    "name": "SH53",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 138,
    "lat1": -28,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SH54.zip",
    "name": "SH54",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 144,
    "lat1": -28,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SH55.zip",
    "name": "SH55",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 150,
    "lat1": -28,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SH56.zip",
    "name": "SH56",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 156,
    "lat1": -28,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/SH57.zip",
    "name": "SH57",
    "area": 24
  },
  {
    "lat0": -32,
    "lng0": 162,
    "lat1": -28,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SH58.zip",
    "name": "SH58",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": -84,
    "lat1": -32,
    "lng1": -78,
    "uri": "http://viewfinderpanoramas.org/dem3/SI17.zip",
    "name": "SI17",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": -78,
    "lat1": -32,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SI18.zip",
    "name": "SI18",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": -72,
    "lat1": -32,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SI19.zip",
    "name": "SI19",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": -66,
    "lat1": -32,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SI20.zip",
    "name": "SI20",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": -60,
    "lat1": -32,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SI21.zip",
    "name": "SI21",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": -54,
    "lat1": -32,
    "lng1": -48,
    "uri": "http://viewfinderpanoramas.org/dem3/SI22.zip",
    "name": "SI22",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 12,
    "lat1": -32,
    "lng1": 18,
    "uri": "http://viewfinderpanoramas.org/dem3/SI33.zip",
    "name": "SI33",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 18,
    "lat1": -32,
    "lng1": 24,
    "uri": "http://viewfinderpanoramas.org/dem3/SI34.zip",
    "name": "SI34",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 24,
    "lat1": -32,
    "lng1": 30,
    "uri": "http://viewfinderpanoramas.org/dem3/SI35.zip",
    "name": "SI35",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 114,
    "lat1": -32,
    "lng1": 120,
    "uri": "http://viewfinderpanoramas.org/dem3/SI50.zip",
    "name": "SI50",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 120,
    "lat1": -32,
    "lng1": 126,
    "uri": "http://viewfinderpanoramas.org/dem3/SI51.zip",
    "name": "SI51",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 126,
    "lat1": -32,
    "lng1": 132,
    "uri": "http://viewfinderpanoramas.org/dem3/SI52.zip",
    "name": "SI52",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 132,
    "lat1": -32,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SI53.zip",
    "name": "SI53",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 138,
    "lat1": -32,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SI54.zip",
    "name": "SI54",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 144,
    "lat1": -32,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SI55.zip",
    "name": "SI55",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 150,
    "lat1": -32,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SI56.zip",
    "name": "SI56",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 168,
    "lat1": -32,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SI59.zip",
    "name": "SI59",
    "area": 24
  },
  {
    "lat0": -36,
    "lng0": 174,
    "lat1": -32,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SI60.zip",
    "name": "SI60",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": -78,
    "lat1": -36,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ18.zip",
    "name": "SJ18",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": -72,
    "lat1": -36,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ19.zip",
    "name": "SJ19",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": -66,
    "lat1": -36,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ20.zip",
    "name": "SJ20",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": -60,
    "lat1": -36,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ21.zip",
    "name": "SJ21",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": -18,
    "lat1": -36,
    "lng1": -12,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ28.zip",
    "name": "SJ28",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": 72,
    "lat1": -36,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ43.zip",
    "name": "SJ43",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": 132,
    "lat1": -36,
    "lng1": 138,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ53.zip",
    "name": "SJ53",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": 138,
    "lat1": -36,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ54.zip",
    "name": "SJ54",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": 144,
    "lat1": -36,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ55.zip",
    "name": "SJ55",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": 150,
    "lat1": -36,
    "lng1": 156,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ56.zip",
    "name": "SJ56",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": 168,
    "lat1": -36,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ59.zip",
    "name": "SJ59",
    "area": 24
  },
  {
    "lat0": -40,
    "lng0": 174,
    "lat1": -36,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SJ60.zip",
    "name": "SJ60",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": -180,
    "lat1": -40,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/SK01.zip",
    "name": "SK01",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": -78,
    "lat1": -40,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SK18.zip",
    "name": "SK18",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": -72,
    "lat1": -40,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SK19.zip",
    "name": "SK19",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": -66,
    "lat1": -40,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SK20.zip",
    "name": "SK20",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": -12,
    "lat1": -40,
    "lng1": -6,
    "uri": "http://viewfinderpanoramas.org/dem3/SK29.zip",
    "name": "SK29",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": 138,
    "lat1": -40,
    "lng1": 144,
    "uri": "http://viewfinderpanoramas.org/dem3/SK54.zip",
    "name": "SK54",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": 144,
    "lat1": -40,
    "lng1": 150,
    "uri": "http://viewfinderpanoramas.org/dem3/SK55.zip",
    "name": "SK55",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": 168,
    "lat1": -40,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SK59.zip",
    "name": "SK59",
    "area": 24
  },
  {
    "lat0": -44,
    "lng0": 174,
    "lat1": -40,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SK60.zip",
    "name": "SK60",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": -180,
    "lat1": -44,
    "lng1": -174,
    "uri": "http://viewfinderpanoramas.org/dem3/SL01.zip",
    "name": "SL01",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": -78,
    "lat1": -44,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SL18.zip",
    "name": "SL18",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": -72,
    "lat1": -44,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SL19.zip",
    "name": "SL19",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": -66,
    "lat1": -44,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SL20.zip",
    "name": "SL20",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": 36,
    "lat1": -44,
    "lng1": 42,
    "uri": "http://viewfinderpanoramas.org/dem3/SL37.zip",
    "name": "SL37",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": 48,
    "lat1": -44,
    "lng1": 54,
    "uri": "http://viewfinderpanoramas.org/dem3/SL39.zip",
    "name": "SL39",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": 162,
    "lat1": -44,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SL58.zip",
    "name": "SL58",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": 168,
    "lat1": -44,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SL59.zip",
    "name": "SL59",
    "area": 24
  },
  {
    "lat0": -48,
    "lng0": 174,
    "lat1": -44,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SL60.zip",
    "name": "SL60",
    "area": 24
  },
  {
    "lat0": -52,
    "lng0": -78,
    "lat1": -48,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SM18.zip",
    "name": "SM18",
    "area": 24
  },
  {
    "lat0": -52,
    "lng0": -72,
    "lat1": -48,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SM19.zip",
    "name": "SM19",
    "area": 24
  },
  {
    "lat0": -52,
    "lng0": -66,
    "lat1": -48,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SM20.zip",
    "name": "SM20",
    "area": 24
  },
  {
    "lat0": -52,
    "lng0": -60,
    "lat1": -48,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SM21.zip",
    "name": "SM21",
    "area": 24
  },
  {
    "lat0": -52,
    "lng0": 66,
    "lat1": -48,
    "lng1": 72,
    "uri": "http://viewfinderpanoramas.org/dem3/SM42.zip",
    "name": "SM42",
    "area": 24
  },
  {
    "lat0": -52,
    "lng0": 162,
    "lat1": -48,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SM58.zip",
    "name": "SM58",
    "area": 24
  },
  {
    "lat0": -52,
    "lng0": 174,
    "lat1": -48,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/dem3/SM60.zip",
    "name": "SM60",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": -78,
    "lat1": -52,
    "lng1": -72,
    "uri": "http://viewfinderpanoramas.org/dem3/SN18.zip",
    "name": "SN18",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": -72,
    "lat1": -52,
    "lng1": -66,
    "uri": "http://viewfinderpanoramas.org/dem3/SN19.zip",
    "name": "SN19",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": -66,
    "lat1": -52,
    "lng1": -60,
    "uri": "http://viewfinderpanoramas.org/dem3/SN20.zip",
    "name": "SN20",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": -60,
    "lat1": -52,
    "lng1": -54,
    "uri": "http://viewfinderpanoramas.org/dem3/SN21.zip",
    "name": "SN21",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": -42,
    "lat1": -52,
    "lng1": -36,
    "uri": "http://viewfinderpanoramas.org/dem3/SN24.zip",
    "name": "SN24",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": -36,
    "lat1": -52,
    "lng1": -30,
    "uri": "http://viewfinderpanoramas.org/dem3/SN25.zip",
    "name": "SN25",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": 0,
    "lat1": -52,
    "lng1": 6,
    "uri": "http://viewfinderpanoramas.org/dem3/SN31.zip",
    "name": "SN31",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": 72,
    "lat1": -52,
    "lng1": 78,
    "uri": "http://viewfinderpanoramas.org/dem3/SN43.zip",
    "name": "SN43",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": 156,
    "lat1": -52,
    "lng1": 162,
    "uri": "http://viewfinderpanoramas.org/dem3/SN57.zip",
    "name": "SN57",
    "area": 24
  },
  {
    "lat0": -56,
    "lng0": 168,
    "lat1": -52,
    "lng1": 174,
    "uri": "http://viewfinderpanoramas.org/dem3/SN59.zip",
    "name": "SN59",
    "area": 24
  },
  {
    "lat0": -60,
    "lng0": -30,
    "lat1": -56,
    "lng1": -24,
    "uri": "http://viewfinderpanoramas.org/dem3/SO26.zip",
    "name": "SO26",
    "area": 24
  },
  {
    "lat0": -64,
    "lng0": -48,
    "lat1": -60,
    "lng1": -42,
    "uri": "http://viewfinderpanoramas.org/dem3/SP23.zip",
    "name": "SP23",
    "area": 24
  },
  {
    "lat0": -68,
    "lng0": 162,
    "lat1": -64,
    "lng1": 168,
    "uri": "http://viewfinderpanoramas.org/dem3/SQ58.zip",
    "name": "SQ58",
    "area": 24
  },
  {
    "lat0": -72,
    "lng0": -96,
    "lat1": -68,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/dem3/SR15.zip",
    "name": "SR15",
    "area": 24
  },
  {
    "lat0": -90,
    "lng0": -180,
    "lat1": -60,
    "lng1": -90,
    "uri": "http://viewfinderpanoramas.org/ANTDEM3/01-15.zip",
    "name": "AN1",
    "area": 2700
  },
  {
    "lat0": -90,
    "lng0": -90,
    "lat1": -60,
    "lng1": 0,
    "uri": "http://viewfinderpanoramas.org/ANTDEM3/16-30.zip",
    "name": "AN2",
    "area": 2700
  },
  {
    "lat0": -90,
    "lng0": 0,
    "lat1": -60,
    "lng1": 90,
    "uri": "http://viewfinderpanoramas.org/ANTDEM3/31-45.zip",
    "name": "AN3",
    "area": 2700
  },
  {
    "lat0": -90,
    "lng0": 90,
    "lat1": -60,
    "lng1": 180,
    "uri": "http://viewfinderpanoramas.org/ANTDEM3/46-60.zip",
    "name": "AN4",
    "area": 2700
  }
]""")

def _isTileMatch(tile, lat, lng):
    """Returns a flag indicating whether the tile contains the specified coordinate"""

    return (tile['lat0'] <= lat < tile['lat1']) and (tile['lng0'] <= lng < tile['lng1'])

def getTile(lat, lng):
    """Gets the tile containing the specified coordinate"""

    matched = list(filter(lambda tile: _isTileMatch(tile, lat, lng), _DEM_TILES))

    matched.sort(key=lambda tile: tile['area'])

    if not matched:
        return None

    return matched[0]
