"""
Iterate through each row of the CSV data file to extract and append
relevant data to a timed OSC bundle.

Data included in the bundle are: the taxi's current latitude and
longitude location, the the start and end longitude and latitude
of the trip leg, the minimum and maximum longitude and latitude
traveled by the taxi over 24 hours, and the number of passengers
currently in the cab.

Timed bundles are decided by scaling the length of the trip leg to
the number of latitude, longitude pairs in the decoded polyline, and
sending out each set of coordinate pairs to Max at each time delay.

Send the bundles of information through the UDP socket and into Max.
"""

from __future__ import division
from OSC import OSCClient, OSCBundle
import csv
import time
import polylinemapper

def unpack(data, totalCoordinates, socket):
    cX = totalCoordinates[0]
    cY = totalCoordinates[1]

    client = OSCClient()
    client.connect(("localhost", socket))

    """ Prepare and send OSC bundles to Max from a list of tuples of coordinates. """
    def bundlePolyline(coordinates, speed, polylineType, passengers, coordsX, coordsY):
        for pair in coordinates:

            # create an OSC bundle:
            bundle = OSCBundle()

            # append polylineType: "trip" or "delay" (data for in between current and next trip)
            bundle.append({'addr': "/curr", 'args': [polylineType]})

            # append min/max longX and latY to bundle:
            bundle.append({'addr': "/minX", 'args': [min(coordsX)]})
            bundle.append({'addr': "/maxX", 'args': [max(coordsX)]})
            bundle.append({'addr': "/minY", 'args': [min(coordsY)]})
            bundle.append({'addr': "/maxY", 'args': [max(coordsY)]})

            # append longX and latY to bundle
            bundle.append({'addr': "/longX", 'args': [pair[0]]})
            bundle.append({'addr': "/latY", 'args': [pair[1]]})
            
            # append start/end longX and latY of coordinates list
            xVals = [coords[0] for coords in coordinates]
            bundle.append({'addr': "/startX", 'args': [xVals[0]]})
            bundle.append({'addr': "/endX", 'args': [xVals[len(xVals) - 1]]})
            yVals = [coords[1] for coords in coordinates]
            bundle.append({'addr': "/startY", 'args': [yVals[0]]})
            bundle.append({'addr': "/endY", 'args': [yVals[len(yVals) - 1]]})

            # append passengers
            bundle.append({'addr': "/passengers", 'args': [passengers]})

            # send bundle to Max:
            client.send(bundle)

            # delay time to even out polyline steps
            time.sleep(speed)

    """ Read the next line in the data file. """
    for row in data:

        """ Parse and set time stamps in minutes (i.e. 4:02 == 242). """
        pickup = row["pickuptime"].split(" ")[1]
        pickup = pickup.split(":")
        pickup = (int(pickup[0])*60) + int(pickup[1])

        dropoff = row["dropofftime"].split(" ")[1]
        dropoff = dropoff.split(":")
        dropoff = (int(dropoff[0])*60) + int(dropoff[1])

        nextPickup = row["nextpickuptime"].split(" ")[1]
        nextPickup = nextPickup.split(":")
        nextPickup = (int(nextPickup[0])*60) + int(nextPickup[1])  

        """ Decode trippolyline. """
        latLongList = polylinemapper.decode(row["trippolyline"])
        passengers = row["passengers"]
        latLongSpeed = round((dropoff - pickup) / (2*len(latLongList)), 10)  # translate 1 minute in RT == 0.5 seconds
        bundlePolyline(latLongList, latLongSpeed, "trip", passengers, cX, cY)

        """ Decode nextpolyline. """
        nextLatLong = polylinemapper.decode(row["nextpolyline"])
        passengers = 0
        nextSpeed = round((nextPickup - dropoff) / (2*len(nextLatLong)), 10)  # translate 1 minute in RT == 0.5 seconds
        bundlePolyline(nextLatLong, nextSpeed, "delay", passengers, cX, cY)

    client.close()
