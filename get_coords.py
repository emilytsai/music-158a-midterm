"""
read CSV file data to decode all polylines in the file; return a list of 
"""
coords_memo = {}

def get_coords(data):
    coordsX = []
    coordsY = []
    for row in data:
        trip = polyline_mapper.decode(row["trippolyline"])
        delay = polyline_mapper.decode(row["nextpolyline"])
        coordsX += [pair[0] for pair in trip]
        coordsX += [pair[0] for pair in delay]
        coordsY += [pair[1] for pair in trip]
        coordsY += [pair[1] for pair in delay]