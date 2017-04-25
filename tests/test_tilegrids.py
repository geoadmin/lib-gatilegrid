# -*- coding: utf-8 -*-

import math
import unittest
from gatilegrid import getTileGrid, GeoadminTileGridLV03, \
    GeoadminTileGridLV95, GlobalMercatorTileGrid, GlobalGeodeticTileGrid


class TestGeoadminTileGrid(unittest.TestCase):

    def testgetTileGrid(self):
        tileGrid = getTileGrid(21781)
        self.assertIs(tileGrid, GeoadminTileGridLV03)
        self.assertIsInstance(tileGrid(), GeoadminTileGridLV03)
        tileGrid = getTileGrid(2056)
        self.assertIs(tileGrid, GeoadminTileGridLV95)
        self.assertIsInstance(tileGrid(), GeoadminTileGridLV95)
        tileGrid = getTileGrid(3857)
        self.assertIs(tileGrid, GlobalMercatorTileGrid)
        self.assertIsInstance(tileGrid(), GlobalMercatorTileGrid)
        tileGrid = getTileGrid(4326)
        self.assertIs(tileGrid, GlobalGeodeticTileGrid)
        self.assertIsInstance(tileGrid(), GlobalGeodeticTileGrid)

    def testUnsupportedTileGrid(self):
        with self.assertRaises(AssertionError):
            getTileGrid(7008)

    def testTileGridWrongExtent(self):
        with self.assertRaises(AssertionError):
            GeoadminTileGridLV03(extent=[10.0, 10.0, 20.0, 20.0])

        with self.assertRaises(AssertionError):
            GeoadminTileGridLV03(
                extent=[430000.0, 40000.0, 420000.0, 340000.0])

    def testTileGridWrongOrigin(self):
        with self.assertRaises(AssertionError):
            GlobalGeodeticTileGrid(originCorner='top-right')

    def testTileSize(self):
        gagrid = GeoadminTileGridLV03()
        ts = gagrid.tileSize(20)
        self.assertEqual(ts, 2560.0)
        self.assertEqual(gagrid.tileAddressTemplate,
                         '{zoom}/{tileCol}/{tileRow}')

        with self.assertRaises(AssertionError):
            gagrid.tileSize(40)

    def testTileBoundsAndAddress(self):
        gagrid = GeoadminTileGridLV03()
        tbe = [548000.0, 196400.0, 573600.0, 222000.0]
        tb = gagrid.tileBounds(17, 5, 5)
        self.assertEqual(tb[0], tbe[0])
        self.assertEqual(tb[1], tbe[1])
        self.assertEqual(tb[2], tbe[2])
        self.assertEqual(tb[3], tbe[3])
        with self.assertRaises(AssertionError):
            gagrid.tileBounds(77, 5, 5)

        ta = gagrid.tileAddress(0, [gagrid.MINX, gagrid.MAXY])
        self.assertEqual(ta[0], 0)
        self.assertEqual(ta[1], 0)
        ta = gagrid.tileAddress(17, [tb[0], tb[3]])
        self.assertEqual(ta[0], 5)
        self.assertEqual(ta[1], 5)

    def testIterGrid(self):
        gagrid = GeoadminTileGridLV03()
        gen = gagrid.iterGrid(0, 0)
        self.assertTrue(hasattr(gen, '__iter__'))
        tileSpec = [t for t in gen]
        self.assertEqual(len(tileSpec), 1)
        self.assertEqual(len(tileSpec[0]), 4)
        self.assertEqual(tileSpec[0][1], 0)
        self.assertEqual(tileSpec[0][2], 0)
        self.assertEqual(tileSpec[0][3], 0)
        self.assertEqual(str(tileSpec[0][0]), str(gagrid.tileBounds(0, 0, 0)))

        gen = gagrid.iterGrid(13, 14)
        tilesSpec = [i for i in gen]
        self.assertEqual(len(tilesSpec), 12)
        self.assertEqual(tilesSpec[0][1], 13)
        self.assertEqual(tilesSpec[6][1], 14)
        bounds = tilesSpec[2][0]
        z = tilesSpec[2][1]
        col = tilesSpec[2][2]
        row = tilesSpec[2][3]
        self.assertEqual(bounds, gagrid.tileBounds(z, col, row))

        with self.assertRaises(AssertionError):
            next(gagrid.iterGrid(13, 33))

        with self.assertRaises(AssertionError):
            next(gagrid.iterGrid(-1, 11))

        with self.assertRaises(AssertionError):
            next(gagrid.iterGrid(13, 11))

    def testGetScale(self):
        gagrid = GeoadminTileGridLV03()
        s14 = gagrid.getScale(14)
        s28 = gagrid.getScale(28)
        self.assertGreater(s14, s28)
        self.assertEqual(round(s14), 2456688.0)
        self.assertEqual(round(s28), 378.0)

    def testGetScaleLV95(self):
        gagrid = GeoadminTileGridLV95()
        s14 = gagrid.getScale(14)
        s28 = gagrid.getScale(28)
        self.assertGreater(s14, s28)
        self.assertEqual(round(s14), 2456688.0)
        self.assertEqual(round(s28), 378.0)

    def testIterGridWithExtent(self):
        offset = 20000.0
        gagridDefault = GeoadminTileGridLV03()
        extent = [gagridDefault.MINX + offset, gagridDefault.MINY + offset,
                  gagridDefault.MAXX - offset, gagridDefault.MAXY - offset]
        gagridExtent = GeoadminTileGridLV03(extent=extent)

        self.assertGreater(gagridDefault.xSpan, gagridExtent.xSpan)
        self.assertGreater(gagridDefault.ySpan, gagridExtent.ySpan)

        tilesSpecDefault = [t for t in gagridDefault.iterGrid(20, 21)]
        tilesSpecExtent = [t for t in gagridExtent.iterGrid(20, 21)]

        self.assertGreater(len(tilesSpecDefault), len(tilesSpecExtent))
        self.assertEqual(tilesSpecExtent[0][1], 20)
        self.assertEqual(tilesSpecExtent[len(tilesSpecExtent) - 1][1], 21)

        nbTiles = gagridExtent.numberOfTilesAtZoom(20) + \
            gagridExtent.numberOfTilesAtZoom(21)
        self.assertEqual(len(tilesSpecExtent), nbTiles)

    def testNumberOfTilesLV03(self):
        zoom = 20
        gagrid = GeoadminTileGridLV03()
        [minRow, minCol, maxRow, maxCol] = gagrid.getExtentAddress(zoom)
        nb = gagrid.numberOfTilesAtZoom(zoom)
        nbx = gagrid.numberOfXTilesAtZoom(zoom)
        nby = gagrid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, maxRow)
        self.assertEqual(len([t for t in gagrid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, 23500)
        self.assertEqual(nb, nbx * nby)
        self.assertGreater(nbx, nby)

        zoom = 22
        [minRow, minCol, maxRow, maxCol] = gagrid.getExtentAddress(zoom)
        nb = gagrid.numberOfTilesAtZoom(zoom)
        nbx = gagrid.numberOfXTilesAtZoom(zoom)
        nby = gagrid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, maxRow)
        self.assertEqual(len([t for t in gagrid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, 375000)
        self.assertEqual(nb, nbx * nby)
        self.assertGreater(nbx, nby)

    def testNumberOfTilesLV95(self):
        zoom = 20
        gagrid = GeoadminTileGridLV95()
        [minRow, minCol, maxRow, maxCol] = gagrid.getExtentAddress(zoom)
        nb = gagrid.numberOfTilesAtZoom(zoom)
        nbx = gagrid.numberOfXTilesAtZoom(zoom)
        nby = gagrid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, maxRow)
        self.assertEqual(len([t for t in gagrid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, 23500)
        self.assertEqual(nb, nbx * nby)
        self.assertGreater(nbx, nby)

        zoom = 22
        [minRow, minCol, maxRow, maxCol] = gagrid.getExtentAddress(zoom)
        nb = gagrid.numberOfTilesAtZoom(zoom)
        nbx = gagrid.numberOfXTilesAtZoom(zoom)
        nby = gagrid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, maxRow)
        self.assertEqual(len([t for t in gagrid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, 375000)
        self.assertEqual(nb, nbx * nby)
        self.assertGreater(nbx, nby)

    def testNumberOfTilesMercator(self):
        grid = GlobalMercatorTileGrid()
        zoom = 0
        nb = grid.numberOfTilesAtZoom(zoom)
        nbx = grid.numberOfXTilesAtZoom(zoom)
        nby = grid.numberOfYTilesAtZoom(zoom)
        self.assertEqual(nb, nbx * nby)
        self.assertEqual(nb, 1)

        zoom = 2
        [minRow, minCol, maxRow, maxCol] = grid.getExtentAddress(zoom)
        nb = grid.numberOfTilesAtZoom(zoom)
        nbx = grid.numberOfXTilesAtZoom(zoom)
        nby = grid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, minCol)
        self.assertGreater(maxRow, minRow)
        self.assertEqual(len([t for t in grid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, nbx * nby)
        self.assertEqual(nb, 16)

    def testNumberOfTilesGeodetic(self):
        grid = GlobalGeodeticTileGrid(originCorner='bottom-left',
                                      tmsCompatible=False)
        zoom = 0
        nb = grid.numberOfTilesAtZoom(zoom)
        nbx = grid.numberOfXTilesAtZoom(zoom)
        nby = grid.numberOfYTilesAtZoom(zoom)
        self.assertEqual(nb, nbx * nby)
        self.assertEqual(nb, 1)

        zoom = 2
        [minRow, minCol, maxRow, maxCol] = grid.getExtentAddress(zoom)
        nb = grid.numberOfTilesAtZoom(zoom)
        nbx = grid.numberOfXTilesAtZoom(zoom)
        nby = grid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, minCol)
        self.assertGreater(maxRow, minRow)
        self.assertEqual(len([t for t in grid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, nbx * nby)
        self.assertEqual(nb, 8)

        grid = GlobalGeodeticTileGrid(originCorner='bottom-left',
                                      tmsCompatible=True)
        zoom = 0
        nb = grid.numberOfTilesAtZoom(zoom)
        nbx = grid.numberOfXTilesAtZoom(zoom)
        nby = grid.numberOfYTilesAtZoom(zoom)
        self.assertEqual(nb, nbx * nby)
        self.assertEqual(nb, 2)

    def testMercatorGridBoundsAndAddress(self):
        grid = GlobalMercatorTileGrid()
        [z, x, y] = [8, 135, 91]
        [xmin, ymin, xmax, ymax] = grid.tileBounds(z, x, y)
        self.assertAlmostEqual(xmin, 1095801.2374962866)
        self.assertAlmostEqual(ymin, 5635549.221409475)
        self.assertAlmostEqual(xmax, 1252344.271424327)
        self.assertAlmostEqual(ymax, 5792092.255337516)

        center = [xmin + (xmax - xmin) / 2, ymin + (ymax - ymin) / 2]
        [xa, ya] = grid.tileAddress(z, center)

        self.assertEqual(xa, x)
        self.assertEqual(ya, y)

    def testGeodeticGridBoundsAndAddress(self):
        grid = GlobalGeodeticTileGrid(originCorner='top-left',
                                      tmsCompatible=True)
        [z, x, y] = [8, 268, 60]
        [xmin, ymin, xmax, ymax] = grid.tileBounds(z, x, y)
        self.assertAlmostEqual(xmin, 8.4375)
        self.assertAlmostEqual(ymin, 47.109375)
        self.assertAlmostEqual(xmax, 9.140625)
        self.assertAlmostEqual(ymax, 47.8125)

        center = [xmin + (xmax - xmin) / 2, ymin + (ymax - ymin) / 2]
        [xa, ya] = grid.tileAddress(z, center)

        self.assertEqual(xa, x)
        self.assertEqual(ya, y)

        [z, x, y] = [8, 266, 193]
        grid = GlobalGeodeticTileGrid(originCorner='bottom-left',
                                      tmsCompatible=True)
        [xmin, ymin, xmax, ymax] = grid.tileBounds(z, x, y)
        self.assertAlmostEqual(xmin, 7.03125)
        self.assertAlmostEqual(ymin, 45.703125)
        self.assertAlmostEqual(xmax, 7.734375)
        self.assertAlmostEqual(ymax, 46.40625)

        center = [xmin + (xmax - xmin) / 2, ymin + (ymax - ymin) / 2]
        [xa, ya] = grid.tileAddress(z, center)

        self.assertEqual(xa, x)
        self.assertEqual(ya, y)
