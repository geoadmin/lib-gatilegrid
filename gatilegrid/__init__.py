from .tilegrids import GeoadminTileGrid, GeoadminTileGridLV95
from .grid import Grid


def getTileGrid(srs):
    assert srs in (21781, 2056), 'Unsupported tile grid'
    if srs == 21781:
        return GeoadminTileGrid
    elif srs == 2056:
        return GeoadminTileGridLV95
