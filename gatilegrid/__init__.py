# -*- coding: utf-8 -*-

import math
from past.builtins import xrange


class GeoadminTileGrid:

    # Defines zooms 0 to 27
    RESOLUTIONS = [
        4000.0,
        3750.0,
        3500.0,
        3250.0,
        3000.0,
        2750.0,
        2500.0,
        2250.0,
        2000.0,
        1750.0,
        1500.0,
        1250.0,
        1000.0,
        750.0,
        650.0,
        500.0,
        250.0,
        100.0,
        50.0,
        20.0,
        10.0,
        5.0,
        2.5,
        2.0,
        1.5,
        1.0,
        0.5,
        0.25,
        0.1
    ]

    # Default Swiss extent
    # For simplicity sake we'll use (x, y) convention
    # when it's really the (y, x) swiss coordinate system we're using
    MINX = 420000.0
    MAXX = 900000.0
    MINY = 30000.0
    MAXY = 350000.0

    XSPAN = MAXX - MINX
    YSPAN = MAXY - MINY

    spatialReference = 21781

    def __init__(self, extent=None, tileSizePx=256.0):
        if extent:
            assert extent[0] < extent[2]
            assert extent[1] < extent[3]
            assert extent[0] >= self.MINX
            assert extent[1] >= self.MINY
            assert extent[2] <= self.MAXX
            assert extent[3] <= self.MAXY
            self.extent = extent
        else:
            self.extent = [self.MINX, self.MINY, self.MAXX, self.MAXY]
        self.origin = [self.extent[0], self.extent[3]]  # Top left corner
        self.tileSizePx = tileSizePx  # In pixels
        self.tileAddressTemplate = '{zoom}/{tileCol}/{tileRow}'

    def tileSize(self, zoom):
        "Returns the size (in meters) of a tile"
        assert zoom in range(0, len(self.RESOLUTIONS))
        return self.tileSizePx * self.RESOLUTIONS[int(zoom)]

    def tileBounds(self, zoom, tileCol, tileRow):
        "Returns the bounds of a tile in LV03 (EPSG:21781)"
        assert zoom in range(0, len(self.RESOLUTIONS))
        # 0,0 at top left: y axis down and x axis right
        tileSize = self.tileSize(zoom)
        minX = self.MINX + (tileCol * tileSize)
        minY = self.MAXY - ((tileRow + 1) * tileSize)
        maxX = self.MINX + ((tileCol + 1) * tileSize)
        maxY = self.MAXY - (tileRow * tileSize)
        return [minX, minY, maxX, maxY]

    def tileAddress(self, zoom, point):
        "Returns a tile address based on a zoom level and \
        a point in the tile"
        [x, y] = point
        assert x <= self.MAXX and x >= self.MINX
        assert y <= self.MAXY and y >= self.MINY
        assert zoom in range(0, len(self.RESOLUTIONS))

        tileS = self.tileSize(zoom)
        offsetX = x - self.MINX
        offsetY = self.MAXY - y
        col = offsetX / tileS
        row = offsetY / tileS
        # We are exactly on the edge of a tile and the extent
        if x in (self.MINX, self.MAXX) and col.is_integer():
            col = max(0, col - 1)
        if y in (self.MINY, self.MAXY) and row.is_integer():
            row = max(0, row - 1)
        return [
            int(math.floor(col)),
            int(math.floor(row))
        ]

    def iterGrid(self, minZoom, maxZoom):
        "Yields the tileBounds, zoom, tileCol and tileRow"
        assert minZoom in range(0, len(self.RESOLUTIONS))
        assert maxZoom in range(0, len(self.RESOLUTIONS))
        assert minZoom <= maxZoom

        for zoom in xrange(minZoom, maxZoom + 1):
            [minRow, minCol, maxRow, maxCol] = self.getExtentAddress(zoom)
            for row in xrange(minRow, maxRow + 1):
                for col in xrange(minCol, maxCol + 1):
                    tileBounds = self.tileBounds(zoom, col, row)
                    yield (tileBounds, zoom, col, row)

    def numberOfXTilesAtZoom(self, zoom):
        "Returns the number of tiles over x at a given zoom level"
        [minRow, minCol, maxRow, maxCol] = self.getExtentAddress(zoom)
        return maxCol - minCol + 1

    def numberOfYTilesAtZoom(self, zoom):
        "Retruns the number of tiles over y at a given zoom level"
        [minRow, minCol, maxRow, maxCol] = self.getExtentAddress(zoom)
        return maxRow - minRow + 1

    def numberOfTilesAtZoom(self, zoom):
        "Returns the total number of tile at a given zoom level"
        [minRow, minCol, maxRow, maxCol] = self.getExtentAddress(zoom)
        return (maxCol - minCol + 1) * (maxRow - minRow + 1)

    def getResolution(self, zoom):
        "Return the image resolution at a given zoom level"
        return self.tileSize(zoom) / self.tileSizePx

    def getScale(self, zoom, dpi=96.0):
        "Return the scale at a given zoom level \
        (1:x e.g. 1 map unit equal x unit in the real world)"
        inchesPerMeters = 39.37
        return self.getResolution(zoom) * inchesPerMeters * dpi

    def getExtentAddress(self, zoom):
        minX = self.extent[0]
        maxY = self.extent[3]
        [minCol, minRow] = self.tileAddress(zoom, [minX, maxY])
        maxX = self.extent[2]
        minY = self.extent[1]
        [maxCol, maxRow] = self.tileAddress(zoom, [maxX, minY])
        return [minRow, minCol, maxRow, maxCol]

    @property
    def xSpan(self):
        "Returns the range in meters over x"
        return self.extent[2] - self.extent[0]

    @property
    def ySpan(self):
        "Returns the range in meters over y"
        return self.extent[3] - self.extent[1]
