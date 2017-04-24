from .tilegrids import GeoadminTileGridLV03, GeoadminTileGridLV95, \
    GlobalMercatorTileGrid, GlobalGeodeticTileGrid
from .grid import Grid


def getTileGrid(srs):
    assert srs in (21781, 2056, 3857, 4326), 'Unsupported tile grid'
    if srs == 21781:
        return GeoadminTileGridLV03
    elif srs == 2056:
        return GeoadminTileGridLV95
    elif srs == 3857:
        return GlobalMercatorTileGrid
    elif srs == 4326:
        return GlobalGeodeticTileGrid
