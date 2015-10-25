"""
read CSV file data to decode all of the polylines in the file
returns a pair of coordinate lists [coordsX, coordsY]
optimze via memoization of data file:coordinates list
"""

import polylineMapper

coords_memo = {}

def get(data):
    if not data in coords_memo:
        coordsX = []
        coordsY = []
        for row in data:
            trip = polylineMapper.decode(row["trippolyline"])
            delay = polylineMapper.decode(row["nextpolyline"])
            coordsX += [pair[0] for pair in trip]
            coordsX += [pair[0] for pair in delay]
            coordsY += [pair[1] for pair in trip]
            coordsY += [pair[1] for pair in delay]
        coords_memo[data] = [coordsX, coordsY]
    return coords_memo[data]
