# -*- coding: utf-8 -*-

import unittest
from gatilegrid import GeodeticTileGrid


class TestGlobalWebmercatorTileGrid(unittest.TestCase):

    def testTileGridWrongExtent(self):
        try:
            GeodeticTileGrid(extent=[ -200.0, -200.0, 0.0, 0.0])
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('GeodeticTileGrid instance: extent assertion error \
                too small not raised')

        try:
            GeodeticTileGrid(extent=[20.0, 50.0, 5.0, 15.0])
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('GeodeticTileGrid instance: extent assertion error \
                inconsistent not raised')


    def testNumberOfTiles(self):
        zoom = 1
        grid = GeodeticTileGrid()
        [minRow, minCol, maxRow, maxCol] = grid.getExtentAddress(zoom)
        nb = grid.numberOfTilesAtZoom(zoom)
        nbx = grid.numberOfXTilesAtZoom(zoom)
        nby = grid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, maxRow)
        self.assertEqual(len([t for t in grid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, 8)
        self.assertEqual(nb, nbx * nby)
        self.assertGreater(nbx, nby)


