# -*- coding: utf-8 -*-

import math
from past.builtins import xrange


EPSG4326_METERS_PER_UNIT = math.pi * 6378137 / 180


class _ResolutionsBase:
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


class _LV03Base(_ResolutionsBase):

    # Default Swiss extent
    # For simplicity sake we'll use (x, y) convention
    # when it's really the (y, x) swiss coordinate system we're using
    MINX = 420000.0
    MAXX = 900000.0
    MINY = 30000.0
    MAXY = 350000.0

    spatialReference = 21781

    tileAddressTemplate = '{zoom}/{tileRow}/{tileCol}'

    unit = 'meters'

    metersPerUnit = 1


class _LV95Base(_ResolutionsBase):

    MINX = 2420000.0
    MAXX = 2900000.0
    MINY = 1030000.0
    MAXY = 1350000.0

    spatialReference = 2056

    tileAddressTemplate = '{zoom}/{tileCol}/{tileRow}'

    unit = 'meters'

    metersPerUnit = 1


class _MercatorBase:
    # origin at the top left a la Google
    # OSGEO:41001 puts the origin at the bottom left
    RESOLUTIONS = [
        156543.03392804097,
        78271.51696402048,
        39135.75848201024,
        19567.87924100512,
        9783.93962050256,
        4891.96981025128,
        2445.98490512564,
        1222.99245256282,
        611.49622628141,
        305.748113140705,
        152.8740565703525,
        76.43702828517625,
        38.21851414258813,
        19.109257071294063,
        9.554628535647032,
        4.777314267823516,
        2.388657133911758,
        1.194328566955879,
        0.5971642834779395,
        0.29858214173896974,
        0.14929107086948487,
        0.07464553543474244,
        0.03732276771737122,
        0.01866138385868561
    ]

    MINX = -20037508.342789244
    MAXX = 20037508.342789244
    MINY = -20037508.342789244
    MAXY = 20037508.342789244

    spatialReference = 3857

    tileAddressTemplate = '{zoom}/{tileCol}/{tileRow}'

    unit = 'meters'

    metersPerUnit = 1


class _GeodeticBase:
    # in arc/pixel
    MINX = -180.0  # lon
    MAXX = 180.0
    MINY = -90.0  # lat
    MAXY = 90.0

    spatialReference = 4326

    tileAddressTemplate = '{zoom}/{tileCol}/{tileRow}'

    unit = 'degrees'

    metersPerUnit = EPSG4326_METERS_PER_UNIT

    def resolutions(self, tmsCompatible, tileSizePx):
        if tmsCompatible:
            self.resFact = 180.0 / tileSizePx  # Cesium terrain
        else:
            self.resFact = 360.0 / tileSizePx  # OpenLayers
        self.RESOLUTIONS = [self.resFact / 2 ** z for z in range(0, 25)]


class _TileGrid(object):

    def __init__(self, extent=None, tileSizePx=256.0, originCorner='top-left',
                 tmsCompatible=None):
        assert originCorner in ('bottom-left', 'top-left')
        self.originCorner = originCorner

        if hasattr(self, 'resolutions') and tmsCompatible is not None:
            self.resolutions(tmsCompatible, tileSizePx)

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
        if self.originCorner == 'bottom-left':
            self.origin = [self.extent[0], self.extent[1]]
        elif self.originCorner == 'top-left':
            self.origin = [self.extent[0], self.extent[3]]
        self.tileSizePx = tileSizePx  # In pixels
        self.XSPAN = self.MAXX - self.MINX
        self.YSPAN = self.MAXY - self.MINY

    def tileSize(self, zoom):
        "Returns the size (in meters) of a tile"
        assert zoom in range(0, len(self.RESOLUTIONS))
        return self.tileSizePx * self.RESOLUTIONS[int(zoom)]

    def tileBounds(self, zoom, tileCol, tileRow):
        "Returns the bounds of a tile in LV03 (EPSG:21781)"
        assert zoom in range(0, len(self.RESOLUTIONS))
        # 0,0 at top left: y axis down and x axis right
        tileSize = self.tileSize(zoom)
        minX = self.MINX + tileCol * tileSize
        maxX = self.MINX + (tileCol + 1) * tileSize
        if self.originCorner == 'bottom-left':
            minY = self.MINY + tileRow * tileSize
            maxY = self.MINY + (tileRow + 1) * tileSize
        elif self.originCorner == 'top-left':
            minY = self.MAXY - (tileRow + 1) * tileSize
            maxY = self.MAXY - tileRow * tileSize
        return [minX, minY, maxX, maxY]

    def tileAddress(self, zoom, point):
        "Returns a tile address based on a zoom level and \
        a point in the tile"
        [x, y] = point
        assert x <= self.MAXX and x >= self.MINX
        assert y <= self.MAXY and y >= self.MINY
        assert zoom in range(0, len(self.RESOLUTIONS))

        tileS = self.tileSize(zoom)
        offsetX = abs(x - self.MINX)
        if self.originCorner == 'bottom-left':
            offsetY = abs(y - self.MINY)
        elif self.originCorner == 'top-left':
            offsetY = abs(self.MAXY - y)
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

    def getZoom(self, resolution):
        "Return the zoom level for a given resolution"
        assert resolution in self.RESOLUTIONS
        return self.RESOLUTIONS.index(resolution)

    def getClosestZoom(self, resolution, unit='meters'):
        "Return the closest zoom level for a given resolution"
        assert unit in ('meters', 'degrees')
        if unit == 'meters' and self.unit == 'degrees':
            resolution = resolution / self.metersPerUnit
        elif unit == 'degrees' and self.unit == 'meters':
            resolution = resolution * EPSG4326_METERS_PER_UNIT
        lo = 0
        hi = len(self.RESOLUTIONS)
        while lo < hi:
            mid = (lo + hi) // 2
            if resolution > self.RESOLUTIONS[mid]:
                hi = mid
            else:
                lo = mid + 1
        if lo == 0:
            return lo
        if hi == len(self.RESOLUTIONS):
            return hi - 1
        before = self.RESOLUTIONS[lo - 1]
        if abs(self.RESOLUTIONS[lo] - resolution) < abs(before - resolution):
            return lo
        return lo - 1

    def getScale(self, zoom):
        if self.unit == 'degrees':
            resolution = self.getResolution(zoom) * EPSG4326_METERS_PER_UNIT
        else:
            resolution = self.getResolution(zoom)
        stdRendPxSize = 0.00028
        return resolution / stdRendPxSize

    def getExtentAddress(self, zoom):
        minX = self.extent[0]
        maxX = self.extent[2]
        if self.originCorner == 'bottom-left':
            minY = self.extent[3]
            maxY = self.extent[1]
        elif self.originCorner == 'top-left':
            minY = self.extent[1]
            maxY = self.extent[3]
        [minCol, minRow] = self.tileAddress(zoom, [minX, maxY])
        [maxCol, maxRow] = self.tileAddress(zoom, [maxX, minY])
        return [minRow, minCol, maxRow, maxCol]

    @property
    def xSpan(self):
        "Returns the range in meters/decimal of arcs over x"
        return abs(self.extent[2] - self.extent[0])

    @property
    def ySpan(self):
        "Returns the range in meters/decimal of arcs over y"
        return abs(self.extent[3] - self.extent[1])


class GeoadminTileGridLV03(_LV03Base, _TileGrid):

    def __init__(self, extent=None, tileSizePx=256.0, originCorner='top-left'):

        super(GeoadminTileGridLV03, self).__init__(
            extent=extent, tileSizePx=tileSizePx, originCorner=originCorner
        )


class GeoadminTileGridLV95(_LV95Base, _TileGrid):

    def __init__(self, extent=None, tileSizePx=256.0, originCorner='top-left'):

        super(GeoadminTileGridLV95, self).__init__(
            extent=extent, tileSizePx=tileSizePx, originCorner=originCorner
        )


class GlobalMercatorTileGrid(_MercatorBase, _TileGrid):

    def __init__(self, extent=None, tileSizePx=256.0, originCorner='top-left'):

        super(GlobalMercatorTileGrid, self).__init__(
            extent=extent, tileSizePx=tileSizePx, originCorner=originCorner
        )


class GlobalGeodeticTileGrid(_GeodeticBase, _TileGrid):

    def __init__(self, extent=None, tileSizePx=256.0, originCorner='top-left',
                 tmsCompatible=True):

        super(GlobalGeodeticTileGrid, self).__init__(
            extent=extent, tileSizePx=tileSizePx, originCorner=originCorner,
            tmsCompatible=tmsCompatible
        )
