from .tilegrids import GeoadminTileGridLV03, GeoadminTileGridLV95
from .tilegrids import GlobalMercatorTileGrid
from .grid import Grid


def getTileGrid(srs):
    assert srs in (21781, 2056, 4326, 3857), 'Unsupported tile grid'
    if srs == 21781:
        return GeoadminTileGridLV03
    elif srs == 2056:
        return GeoadminTileGridLV95
    elif srs == 3857:
        return GlobalMercatorTileGrid
