# -*- coding: utf-8 -*-

import unittest
from gatilegrid import GlobalWebmercatorTileGrid


class TestGlobalWebmercatorTileGrid(unittest.TestCase):

    def testTileGridWrongExtent(self):
        try:
            GlobalWebmercatorTileGrid(extent=[ -30e6, -30e6, 0, 0])
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('GlobalWebmercatorTileGrid instance: extent assertion error \
                too small not raised')

        try:
            GlobalWebmercatorTileGrid(extent=[430000.0, 40000.0, 420000.0, 340000.0])
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('GlobalWebmercatorTileGrid instance: extent assertion error \
                inconsistent not raised')


    def testNumberOfTiles(self):
        zoom = 1
        webmercatorgrid = GlobalWebmercatorTileGrid()
        [minRow, minCol, maxRow, maxCol] = webmercatorgrid.getExtentAddress(zoom)
        nb = webmercatorgrid.numberOfTilesAtZoom(zoom)
        nbx = webmercatorgrid.numberOfXTilesAtZoom(zoom)
        nby = webmercatorgrid.numberOfYTilesAtZoom(zoom)
        self.assertEqual(maxCol, maxRow)
        self.assertEqual(len([t for t in webmercatorgrid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, 4)
        self.assertEqual(nb, nbx * nby)
        self.assertEqual(nbx, nby)


