# -*- coding: utf-8 -*-

import math
from past.builtins import xrange


class Grid:
    #   parameters:
    #   extent [minX, minY, maxX, maxY]
    #   resolutionX (signed resolution over x-axis)
    #   resolutionY (signed resolution over y-axis)

    #   case origin isTopLeft

    #   a=(col=0,row=0)
    #   b=(col=i,row=0)
    #   c=(col=0,row=j)
    #   d=(col=i,row=j)

    #   a_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ b_    #
    #   |_|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ |_|   #
    #   |                                  |   #
    #   |                                  |   #
    #   |                                  |   #
    #   |                                  |   #
    #   c_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ d_|   #
    #   |_|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ |_|   #

    def __init__(self, extent, resolutionX, resolutionY):
        self.extent = [float(e) for e in extent]
        self.resolutionX = float(resolutionX)
        self.resolutionY = float(resolutionY)
        self._setOrigin()
        self._setExtentAddress()

    def __iter__(self):
        for col in xrange(0, self.nbCellsX):
            for row in xrange(0, self.nbCellsY):
                cellExtent = self.cellExtent(col, row)
                yield (cellExtent, col, row)

    def cellExtent(self, col, row):
        if self.isLeft:
            minX = self.MINX + (col * self.resolutionX)
            maxX = self.MINX + ((col + 1) * self.resolutionX)
        elif self.isRight:
            minX = self.MAXX + ((col + 1) * self.resolutionX)
            maxX = self.MAXY + (col * self.resolutionX)

        if self.isBottom:
            minY = self.MINY + (row * self.resolutionY)
            maxY = self.MINY + ((row + 1) * self.resolutionY)
        elif self.isTop:
            minY = self.MAXY + ((row + 1) * self.resolutionY)
            maxY = self.MAXY + (row * self.resolutionY)

        return [minX, minY, maxX, maxY]

    def cellAddressFromPointCoordinate(self, pointCoordinate):
        if not self.inExtent(pointCoordinate):
            return [None, None]

        [x, y] = pointCoordinate

        if self.isLeft:
            offsetX = x - self.MINX
        elif self.isRight:
            offsetX = self.MAXX - x

        if self.isBottom:
            offsetY = y - self.MINY
        elif self.isTop:
            offsetY = self.MAXY - y

        col = abs(offsetX / self.resolutionX)
        row = abs(offsetY / self.resolutionY)
        if x in (self.MINX, self.MAXX) and col.is_integer():
            col = max(0, col - 1)
        if y in (self.MINY, self.MAXY) and row.is_integer():
            row = max(0, row - 1)
        return [
            int(math.floor(col)),
            int(math.floor(row))
        ]

    def getExtentAddress(self, extent):
        fromCellCoordinate = extent[:2]
        toCellCoordinate = extent[2:4]
        colFrom, rowFrom = \
            self.cellAddressFromPointCoordinate(fromCellCoordinate)
        colTo, rowTo = \
            self.cellAddressFromPointCoordinate(toCellCoordinate)
        return [min(colFrom, colTo), min(rowFrom, rowTo),
                max(colFrom, colTo), max(rowFrom, rowTo)]

    def inExtent(self, pointCoordinate):
        [x, y] = pointCoordinate
        return x >= self.MINX and x <= self.MAXX and \
            y >= self.MINY and y <= self.MAXY

    def _setOrigin(self):
        if self.isBottomLeft:
            self.origin = [self.extent[0], self.extent[1]]
            self.end = [self.extent[2], self.extent[3]]
        elif self.isBottomRight:
            self.origin = [self.extent[2], self.extent[1]]
            self.end = [self.extent[0], self.extent[3]]
        elif self.isTopLeft:
            self.origin = [self.extent[0], self.extent[3]]
            self.end = [self.extent[2], self.extent[1]]
        elif self.isTopRight:
            self.origin = [self.extent[2], self.extent[3]]
            self.end = [self.extent[0], self.extent[1]]

    def _setExtentAddress(self):
        [minCol, minRow] = self.cellAddressFromPointCoordinate(self.origin)
        [maxCol, maxRow] = self.cellAddressFromPointCoordinate(self.end)
        self.extentAddress = [minCol, minRow, maxCol, maxRow]

    @property
    def cellArea(self):
        return abs(self.resolutionX * self.resolutionY)

    @property
    def nbCellsX(self):
        [minCol, minRow, maxCol, maxRow] = self.extentAddress
        return maxCol + 1

    @property
    def nbCellsY(self):
        [minCol, minRow, maxCol, maxRow] = self.extentAddress
        return maxRow + 1

    @property
    def nbCells(self):
        return self.nbCellsX * self.nbCellsY

    @property
    def isLeft(self):
        return self.resolutionX > 0

    @property
    def isRight(self):
        return self.resolutionX < 0

    @property
    def isBottom(self):
        return self.resolutionY > 0

    @property
    def isTop(self):
        return self.resolutionY < 0

    @property
    def isTopLeft(self):
        return self.isTop and self.isLeft

    @property
    def isBottomLeft(self):
        return self.isBottom and self.isLeft

    @property
    def isTopRight(self):
        return self.isTop and self.isRight

    @property
    def isBottomRight(self):
        return self.isBottom and self.isRight

    @property
    def MINX(self):
        return self.extent[0]

    @property
    def MAXX(self):
        return self.extent[2]

    @property
    def MINY(self):
        return self.extent[1]

    @property
    def MAXY(self):
        return self.extent[3]
