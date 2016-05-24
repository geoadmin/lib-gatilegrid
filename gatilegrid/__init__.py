# -*- coding: utf-8 -*-

import math
from past.builtins import xrange


class TileGrid(object):

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

    def __init__(self, extent=None, gridExtent=(MINX, MINY, MAXX, MAXY), resolutions=RESOLUTIONS, tileSizePx=256.0, spatialReference=21781):
        self.MINX, self.MINY, self.MAXX, self.MAXY = gridExtent
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
        self.resolutions = resolutions if resolutions is not None else self.resolutions()
        self.spatialReference = spatialReference
        self.gridExtent = gridExtent

    def resolutions(self, min_res=None, max_res=None, res_factor=2.0, num_levels=None,
                    bbox=None, tile_size=(256, 256)):
        if res_factor == 'sqrt2':
            res_factor = math.sqrt(2)
        bbox = self.gridExtent

        res = []
        if not min_res:
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            min_res = max(width / tile_size[0], height / tile_size[1])

        if max_res:
            if num_levels:
                res_step = (math.log10(min_res) - math.log10(max_res)) / (num_levels - 1)
                res = [10**(math.log10(min_res) - res_step * i) for i in range(num_levels)]
            else:
                res = [min_res]
                while True:
                    next_res = res[-1] / res_factor
                    if max_res >= next_res:
                        break
                    res.append(next_res)
        else:
            if not num_levels:
                num_levels = 20 if res_factor != math.sqrt(2) else 40
            res = [min_res]
            while len(res) < num_levels:
                res.append(res[-1] / res_factor)

        return res

    def tileSize(self, zoom):
        "Returns the size (in meters) of a tile"
        assert zoom in range(0, len(self.resolutions))
        return self.tileSizePx * self.resolutions[int(zoom)]

    def tileBounds(self, zoom, tileCol, tileRow):
        "Returns the bounds of a tile in LV03 (EPSG:21781)"
        assert zoom in range(0, len(self.resolutions))
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
        assert zoom in range(0, len(self.resolutions))

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
        assert minZoom in range(0, len(self.resolutions))
        assert maxZoom in range(0, len(self.resolutions))
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


class GeoadminTileGrid(TileGrid):

    def __init__(self, extent=None, tileSizePx=256.0):

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
        gridExtent = (MINX, MINY, MAXX, MAXY)
        resolutions = RESOLUTIONS
        spatialReference = 21781

        super(GeoadminTileGrid, self).__init__(extent=extent, gridExtent=(MINX, MINY, MAXX, MAXY), resolutions=RESOLUTIONS, tileSizePx=tileSizePx, spatialReference=21781)


class GlobalWebmercatorTileGrid(TileGrid):

    def __init__(self, extent=None, tileSizePx=256.0):

        # Global Web Mercator Grid, compatible with OSM map, etc.

        MINX = -20037508.342789244
        MAXX = 20037508.342789244
        MINY = -20037508.342789244
        MAXY = 20037508.342789244

        XSPAN = MAXX - MINX
        YSPAN = MAXY - MINY

        spatialReference = 3857
        gridExtent = (MINX, MINY, MAXX, MAXY)
        resolutions = [156543.03392804097, 78271.51696402048, 39135.75848201024, 19567.87924100512, 9783.93962050256, 4891.96981025128, 2445.98490512564, 1222.99245256282, 611.49622628141, 305.748113140705, 152.8740565703525, 76.43702828517625, 38.21851414258813, 19.109257071294063, 9.554628535647032, 4.777314267823516, 2.388657133911758, 1.194328566955879, 0.5971642834779395, 0.29858214173896974, 0.14929107086948487, 0.07464553543474244, 0.03732276771737122, 0.01866138385868561]
        spatialReference = 3857

        super(GlobalWebmercatorTileGrid, self).__init__(extent=extent, gridExtent=(MINX, MINY, MAXX, MAXY), resolutions=resolutions, tileSizePx=tileSizePx, spatialReference=3857)


class GeodeticTileGrid(TileGrid):

    def __init__(self, extent=None, tileSizePx=256.0):

        # Global Geodetic Grid, with two tiles at zoom level 0

        MINX = -180.0
        MAXX = 180.0
        MINY = -90.0
        MAXY = 90.0

        XSPAN = MAXX - MINX
        YSPAN = MAXY - MINY

        self.spatialReference = 4326
        self.gridExtent = (MINX, MINY, MAXX, MAXY)
        resolutions = [0.703125, 0.3515625, 0.17578125, 0.087890625, 0.0439453125, 0.02197265625, 0.010986328125, 0.0054931640625, 0.00274658203125, 0.001373291015625, 0.0006866455078125, 0.00034332275390625, 0.000171661376953125, 8.58306884765625e-05, 4.291534423828125e-05, 2.1457672119140625e-05, 1.0728836059570312e-05, 5.364418029785156e-06, 2.682209014892578e-06]

        super(GeodeticTileGrid, self).__init__(extent=extent, gridExtent=(MINX, MINY, MAXX, MAXY), resolutions=resolutions, tileSizePx=tileSizePx, spatialReference=3857)
