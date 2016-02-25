# -*- coding: utf-8 -*-

import math


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
        minX = self.MINX + (tileCol * self.tileSize(zoom))
        minY = self.MAXY - ((tileRow + 1) * self.tileSize(zoom))
        maxX = self.MINX + ((tileCol + 1) * self.tileSize(zoom))
        maxY = self.MAXY - (tileRow * self.tileSize(zoom))
        return [minX, minY, maxX, maxY]

    def tileAddress(self, zoom, topLeft):
        "Returns a tile address based on a zoom level and \
        the top left coordinate of a tile"
        [x, y] = topLeft
        assert x <= self.MAXX and x >= self.MINX
        assert y <= self.MAXY and y >= self.MINY
        assert zoom in range(0, len(self.RESOLUTIONS))

        tileS = self.tileSize(zoom)
        offsetX = self.XSPAN - (self.MAXX - x)
        offsetY = self.YSPAN - (y - self.MINY)
        totNbTilesX = math.ceil(self.XSPAN / tileS)
        totNbTilesY = math.ceil(self.YSPAN / tileS)
        return [
            int(round((offsetX / self.XSPAN) * totNbTilesX)),  # Row
            int(round((offsetY / self.YSPAN) * totNbTilesY))  # Col
        ]

    def iterGrid(self, minZoom, maxZoom):
        "Yields the tileBounds, zoom, tileCol and tileRow"
        assert minZoom in range(0, len(self.RESOLUTIONS))
        assert maxZoom in range(0, len(self.RESOLUTIONS))
        assert minZoom <= maxZoom

        for zoom in range(minZoom, maxZoom + 1):
            maxX = self.extent[2]
            minY = self.extent[1]
            [tileRow, tileCol] = self.tileAddress(zoom, self.origin)
            while self.extent[2] >= maxX:
                while self.extent[1] <= minY:
                    tileBounds = self.tileBounds(zoom, tileCol, tileRow)
                    [minX, minY, maxX, maxY] = tileBounds
                    yield (tileBounds, zoom, tileCol, tileRow)
                    tileRow += 1
                minY = self.extent[1]
                tileCol += 1
                tileRow = 0

    def numberOfXTilesAtZoom(self, zoom):
        "Returns the number of tiles over x at a given zoom level"
        return int(math.ceil(self.xSpan / self.tileSize(zoom)))

    def numberOfYTilesAtZoom(self, zoom):
        "Retrurns the number of tiles over y at a given zoom level"
        return int(math.ceil(self.ySpan / self.tileSize(zoom)))

    def numberOfTilesAtZoom(self, zoom):
        "Returns the total number of tile at a given zoom level"
        return self.numberOfXTilesAtZoom(zoom) * \
            self.numberOfYTilesAtZoom(zoom)

    def getResolution(self, zoom):
        "Return the image resolution at a given zoom level"
        return self.tileSize(zoom) / self.tileSizePx

    def getScale(self, zoom, dpi=96.0):
        "Return the scale at a given zoom level \
        (1:x e.g. 1 map unit equal x unit in the real world)"
        inchesPerMeters = 39.37
        return self.getResolution(zoom) * inchesPerMeters * dpi

    @property
    def xSpan(self):
        "Returns the range in meters over x"
        return self.extent[2] - self.extent[0]

    @property
    def ySpan(self):
        "Returns the range in meters over y"
        return self.extent[3] - self.extent[1]
