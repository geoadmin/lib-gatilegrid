import unittest
from gatilegrid.grid import Grid


class TestGeoadminTileGrid(unittest.TestCase):

    def testGridBottomLeft(self):
        extent = [minx, miny, maxx, maxy] = [0, 0, 100, 100]
        resolutionX = 5
        resolutionY = 5
        grid = Grid(extent, resolutionX, resolutionY)

        self.assertTrue(grid.isBottomLeft)
        self.assertEqual(grid.cellArea, resolutionX * resolutionY)

        col = 0
        row = 0
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, minx)
        self.assertEqual(cminy, miny)
        self.assertEqual(cmaxx, resolutionX)
        self.assertEqual(cmaxy, resolutionY)

        col = 0
        row = 1
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, minx)
        self.assertEqual(cminy, resolutionY)
        self.assertEqual(cmaxx, resolutionX)
        self.assertEqual(cmaxy, 2 * resolutionY)

        col = 1
        row = 0
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, resolutionX)
        self.assertEqual(cminy, miny)
        self.assertEqual(cmaxx, 2 * resolutionX)
        self.assertEqual(cmaxy, resolutionY)

        nbCells = grid.nbCells
        nbCellsX = grid.nbCellsX
        nbCellsY = grid.nbCellsY
        self.assertEqual(nbCellsX, (maxx - minx) / resolutionX)
        self.assertEqual(nbCellsY, (maxy - miny) / resolutionY)
        self.assertEqual(nbCells, nbCellsX * nbCellsY)

        gridCellsSpec = [s for s in grid]
        self.assertEqual(nbCells, len(gridCellsSpec))
        col = 0
        row = 0
        self.assertEqual(gridCellsSpec[0][1], col)
        self.assertEqual(gridCellsSpec[0][2], row)

        [col, row] = grid.cellAddressFromPointCoordinate([0, 0])
        self.assertEqual(col, 0)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([1, 1])
        self.assertEqual(col, 0)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([5, 5])
        self.assertEqual(col, 1)
        self.assertEqual(row, 1)

        [col, row] = grid.cellAddressFromPointCoordinate([7.5, 5])
        self.assertEqual(col, 1)
        self.assertEqual(row, 1)

        [minCol, minRow, maxCol, maxRow] = grid.extentAddress
        self.assertEqual(gridCellsSpec[nbCells - 1][1], maxCol)
        self.assertEqual(gridCellsSpec[nbCells - 1][2], maxRow)

        cellOutsideExtent = [200, 200]
        [col, row] = grid.cellAddressFromPointCoordinate(cellOutsideExtent)
        self.assertEqual(col, None)
        self.assertEqual(row, None)

        extentAddress = grid.getExtentAddress(extent)
        self.assertEqual(grid.extentAddress[0], extentAddress[0])
        self.assertEqual(grid.extentAddress[1], extentAddress[1])
        self.assertEqual(grid.extentAddress[2], extentAddress[2])
        self.assertEqual(grid.extentAddress[3], extentAddress[3])

        extent_sub = [20, 20, 40, 40]
        extentAddress_sub = grid.getExtentAddress(extent_sub)
        self.assertLess(extentAddress[0], extentAddress_sub[0])
        self.assertLess(extentAddress[1], extentAddress_sub[1])
        self.assertGreater(extentAddress[2], extentAddress_sub[2])
        self.assertGreater(extentAddress[3], extentAddress_sub[3])

    def testGridTopLeft(self):
        extent = [minx, miny, maxx, maxy] = [0, 0, 100, 100]
        resolutionX = 5
        resolutionY = -5
        grid = Grid(extent, resolutionX, resolutionY)

        self.assertTrue(grid.isTopLeft)
        self.assertEqual(grid.cellArea, abs(resolutionX * resolutionY))

        col = 0
        row = 0
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, minx)
        self.assertEqual(cminy, maxy + resolutionY)
        self.assertEqual(cmaxx, resolutionX)
        self.assertEqual(cmaxy, maxy)

        col = 0
        row = 1
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, minx)
        self.assertEqual(cminy, maxy + (2 * resolutionY))
        self.assertEqual(cmaxx, resolutionX)
        self.assertEqual(cmaxy, maxy + resolutionY)

        col = 1
        row = 0
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, resolutionX)
        self.assertEqual(cminy, maxy + resolutionY)
        self.assertEqual(cmaxx, 2 * resolutionX)
        self.assertEqual(cmaxy, maxy)

        nbCells = grid.nbCells
        nbCellsX = grid.nbCellsX
        nbCellsY = grid.nbCellsY
        self.assertEqual(nbCellsX, abs((maxx - minx) / resolutionX))
        self.assertEqual(nbCellsY, abs((maxy - miny) / resolutionY))
        self.assertEqual(nbCells, nbCellsX * nbCellsY)

        gridCellsSpec = [s for s in grid]
        self.assertEqual(nbCells, len(gridCellsSpec))
        col = 0
        row = 0
        self.assertEqual(gridCellsSpec[0][1], col)
        self.assertEqual(gridCellsSpec[0][2], row)

        [col, row] = grid.cellAddressFromPointCoordinate([0, 100])
        self.assertEqual(col, 0)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([1, 99])
        self.assertEqual(col, 0)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([5, 95])
        self.assertEqual(col, 1)
        self.assertEqual(row, 1)

        [col, row] = grid.cellAddressFromPointCoordinate([7.5, 95])
        self.assertEqual(col, 1)
        self.assertEqual(row, 1)

        [minCol, minRow, maxCol, maxRow] = grid.extentAddress
        self.assertEqual(gridCellsSpec[nbCells - 1][1], maxCol)
        self.assertEqual(gridCellsSpec[nbCells - 1][2], maxRow)

        cellOutsideExtent = [200, 200]
        [col, row] = grid.cellAddressFromPointCoordinate(cellOutsideExtent)
        self.assertEqual(col, None)
        self.assertEqual(row, None)

        extentAddress = grid.getExtentAddress(extent)
        self.assertEqual(grid.extentAddress[0], extentAddress[0])
        self.assertEqual(grid.extentAddress[1], extentAddress[1])
        self.assertEqual(grid.extentAddress[2], extentAddress[2])
        self.assertEqual(grid.extentAddress[3], extentAddress[3])

        extent_sub = [20, 20, 40, 40]
        extentAddress_sub = grid.getExtentAddress(extent_sub)
        self.assertLess(extentAddress[0], extentAddress_sub[0])
        self.assertLess(extentAddress[1], extentAddress_sub[1])
        self.assertGreater(extentAddress[2], extentAddress_sub[2])
        self.assertGreater(extentAddress[3], extentAddress_sub[3])

    def testGridTopRight(self):
        extent = [minx, miny, maxx, maxy] = [0, 0, 100, 100]
        resolutionX = -5
        resolutionY = -5
        grid = Grid(extent, resolutionX, resolutionY)

        self.assertTrue(grid.isTopRight)
        self.assertEqual(grid.cellArea, abs(resolutionX * resolutionY))

        col = 0
        row = 0
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, maxx + resolutionX)
        self.assertEqual(cminy, maxy + resolutionY)
        self.assertEqual(cmaxx, maxx)
        self.assertEqual(cmaxy, maxy)

        col = 0
        row = 1
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, maxx + resolutionX)
        self.assertEqual(cminy, maxy + (2 * resolutionY))
        self.assertEqual(cmaxx, maxx)
        self.assertEqual(cmaxy, maxy + resolutionY)

        col = 1
        row = 0
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, maxx + (2 * resolutionX))
        self.assertEqual(cminy, maxy + resolutionY)
        self.assertEqual(cmaxx, maxx + resolutionX)
        self.assertEqual(cmaxy, maxy)

        nbCells = grid.nbCells
        nbCellsX = grid.nbCellsX
        nbCellsY = grid.nbCellsY
        self.assertEqual(nbCellsX, abs((maxx - minx) / resolutionX))
        self.assertEqual(nbCellsY, abs((maxy - miny) / resolutionY))
        self.assertEqual(nbCells, nbCellsX * nbCellsY)

        gridCellsSpec = [s for s in grid]
        self.assertEqual(nbCells, len(gridCellsSpec))
        col = 0
        row = 0
        self.assertEqual(gridCellsSpec[0][1], col)
        self.assertEqual(gridCellsSpec[0][2], row)

        maxCol = abs((maxx - minx) / resolutionX) - 1
        [col, row] = grid.cellAddressFromPointCoordinate([100, 100])
        self.assertEqual(col, 0)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([0, 100])
        self.assertEqual(col, maxCol)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([1, 99])
        self.assertEqual(col, maxCol)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([5, 95])
        self.assertEqual(col, maxCol)
        self.assertEqual(row, 1)

        [col, row] = grid.cellAddressFromPointCoordinate([7.5, 95])
        self.assertEqual(col, maxCol - 1)
        self.assertEqual(row, 1)

        [minCol, minRow, maxCol, maxRow] = grid.extentAddress
        self.assertEqual(gridCellsSpec[nbCells - 1][1], maxCol)
        self.assertEqual(gridCellsSpec[nbCells - 1][2], maxRow)

        cellOutsideExtent = [200, 200]
        [col, row] = grid.cellAddressFromPointCoordinate(cellOutsideExtent)
        self.assertEqual(col, None)
        self.assertEqual(row, None)

        extentAddress = grid.getExtentAddress(extent)
        self.assertEqual(grid.extentAddress[0], extentAddress[0])
        self.assertEqual(grid.extentAddress[1], extentAddress[1])
        self.assertEqual(grid.extentAddress[2], extentAddress[2])
        self.assertEqual(grid.extentAddress[3], extentAddress[3])

        extent_sub = [20, 20, 40, 40]
        extentAddress_sub = grid.getExtentAddress(extent_sub)
        self.assertLess(extentAddress[0], extentAddress_sub[0])
        self.assertLess(extentAddress[1], extentAddress_sub[1])
        self.assertGreater(extentAddress[2], extentAddress_sub[2])
        self.assertGreater(extentAddress[3], extentAddress_sub[3])

    def testGridBottomRight(self):
        extent = [minx, miny, maxx, maxy] = [0, 0, 100, 100]
        resolutionX = -5
        resolutionY = 5
        grid = Grid(extent, resolutionX, resolutionY)

        self.assertTrue(grid.isBottomRight)
        self.assertEqual(grid.cellArea, abs(resolutionX * resolutionY))

        col = 0
        row = 0
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, maxx + resolutionX)
        self.assertEqual(cminy, miny)
        self.assertEqual(cmaxx, maxx)
        self.assertEqual(cmaxy, miny + resolutionY)

        col = 0
        row = 1
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, maxx + resolutionX)
        self.assertEqual(cminy, miny + resolutionY)
        self.assertEqual(cmaxx, maxx)
        self.assertEqual(cmaxy, miny + (2 * resolutionY))

        col = 1
        row = 0
        [cminx, cminy, cmaxx, cmaxy] = grid.cellExtent(col, row)
        self.assertEqual(cminx, maxx + (2 * resolutionX))
        self.assertEqual(cminy, miny)
        self.assertEqual(cmaxx, maxx + resolutionX)
        self.assertEqual(cmaxy, miny + resolutionY)

        nbCells = grid.nbCells
        nbCellsX = grid.nbCellsX
        nbCellsY = grid.nbCellsY
        self.assertEqual(nbCellsX, abs((maxx - minx) / resolutionX))
        self.assertEqual(nbCellsY, abs((maxy - miny) / resolutionY))
        self.assertEqual(nbCells, nbCellsX * nbCellsY)

        gridCellsSpec = [s for s in grid]
        self.assertEqual(nbCells, len(gridCellsSpec))
        col = 0
        row = 0
        self.assertEqual(gridCellsSpec[0][1], col)
        self.assertEqual(gridCellsSpec[0][2], row)

        [col, row] = grid.cellAddressFromPointCoordinate([100, 0])
        self.assertEqual(col, 0)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([99, 1])
        self.assertEqual(col, 0)
        self.assertEqual(row, 0)

        [col, row] = grid.cellAddressFromPointCoordinate([94, 6])
        self.assertEqual(col, 1)
        self.assertEqual(row, 1)

        maxCol = abs(((maxy - miny) / resolutionY)) - 1
        [col, row] = grid.cellAddressFromPointCoordinate([100, 100])
        self.assertEqual(col, 0)
        self.assertEqual(row, maxCol)

        [minCol, minRow, maxCol, maxRow] = grid.extentAddress
        self.assertEqual(gridCellsSpec[nbCells - 1][1], maxCol)
        self.assertEqual(gridCellsSpec[nbCells - 1][2], maxRow)

        cellOutsideExtent = [200, 200]
        [col, row] = grid.cellAddressFromPointCoordinate(cellOutsideExtent)
        self.assertEqual(col, None)
        self.assertEqual(row, None)

        extentAddress = grid.getExtentAddress(extent)
        self.assertEqual(grid.extentAddress[0], extentAddress[0])
        self.assertEqual(grid.extentAddress[1], extentAddress[1])
        self.assertEqual(grid.extentAddress[2], extentAddress[2])
        self.assertEqual(grid.extentAddress[3], extentAddress[3])

        extent_sub = [20, 20, 40, 40]
        extentAddress_sub = grid.getExtentAddress(extent_sub)
        self.assertLess(extentAddress[0], extentAddress_sub[0])
        self.assertLess(extentAddress[1], extentAddress_sub[1])
        self.assertGreater(extentAddress[2], extentAddress_sub[2])
        self.assertGreater(extentAddress[3], extentAddress_sub[3])
