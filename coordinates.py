"""
Read the entire CSV file data to decode all of the polylines in the file
(if not yet in the memoized coordinates list).

Return a list of a pair of lists containing all X coordinates and Y coordinates
[coordsX, coordsY].

Optimze function via memoization of data file:coordinates list.
"""

import polylinemapper

coordsMemo = {}

""" Get the corresponding coordinates list value from the coordsMemo
that is held by the datafile name as the key. """
def get(data):
    if not data in coordsMemo:
        coordsX = []
        coordsY = []
        for row in data:
            trip = polylinemapper.decode(row["trippolyline"])
            delay = polylinemapper.decode(row["nextpolyline"])
            coordsX += [pair[0] for pair in trip]
            coordsX += [pair[0] for pair in delay]
            coordsY += [pair[1] for pair in trip]
            coordsY += [pair[1] for pair in delay]
        coordsMemo[data] = [coordsX, coordsY]
    return coordsMemo[data]
