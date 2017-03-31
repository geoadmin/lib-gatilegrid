gatilegrid
===========

[![Build Status](https://travis-ci.org/geoadmin/gatilegrid.svg?branch=master)](https://travis-ci.org/geoadmin/gatilegrid)

## Geoadmin custom tile grid for web mapping applications

gatilegrid is compatible with python 2.7 and 3.5

### Usage

```python
from gatilegrid import GeoadminTileGrid

zoom = 18
tileCol = 6
tileRow = 7

gagrid = GeoadminTileGrid()
# With extent constraint
offset = 100000
gagridExtent = GeoadminTileGrid(extent=[gagrid.MINX + offset, gagrid.MINY + offset,
                                        gagrid.MAXX - offset, gagrid.MAXY - offset])

bounds = [xmin, ymin, xmax, ymax] = gagrid.tileBounds(zoom, tileCol, tileRow)
print bounds
print gagrid.tileAddressTemplate
>>>> [496800.0, 247600.0, 509600.0, 260400.0]
>>>> {zoom}/{tileCol}/{tileRow}

topLeftCorner = [xmin, ymax]
tileAddress = [tileCol, tileRow] = gagrid.tileAddress(zoom, topLeftCorner)
print tileAddress
>>>> [7, 6]

# It also works if the point is within the tile
pointInTile = [topLeftCorner[0] + 200.0, topLeftCorner[1] - 200.0]
print gagrid.tileAddress(zoom, pointInTile)
>>>> [7, 6]

# Resolution in meters
print gagrid.getResolution(zoom)
>>>> 50.0

# Scale dpi dependent (defaults to 96)
print gagrid.getScale(zoom, dpi=96.0)
>>>> 188976.0

# Tile size in meters
print gagrid.tileSize(zoom)
>>>> 12800.0

# Number of tiles at zoom
print gagrid.numberOfTilesAtZoom(zoom)
>>>> 950
# Extent dependent
print gagridExtent.numberOfTilesAtZoom(zoom)
>>>> 253

# Generate tilesSpec
counter = 0
minZoom = 16
maxZoom = zoom
tilesSpecGenerator = gagrid.iterGrid(minZoom, maxZoom)
for t in tilesSpecGenerator:
    (tileBounds, zoom, tileCol, tileRow) = t
    print t
    counter += 1
    if counter == 2:
        break
>>>> ([420000.0, 286000.0, 484000.0, 350000.0], 16, 0, 0)
>>>> ([484000.0, 286000.0, 548000.0, 350000.0], 16, 1, 0)
# Extent dependent
counter = 0
tilesSpecGeneratorExtent = gagridExtent.iterGrid(minZoom, maxZoom)
for t in tilesSpecGeneratorExtent:
    (tileBounds, zoom, tileCol, tileRow) = t
    print t
    counter += 1
    if counter == 2:
        break
>>>> ([484000.0, 222000.0, 548000.0, 286000.0], 16, 1, 1)
>>>> ([548000.0, 222000.0, 612000.0, 286000.0], 16, 2, 1)

```

### Tests

```
python setup.py test

```

####CONTRIBUTORS:

- [Loïc Gasser](https://github.com/loicgasser)
