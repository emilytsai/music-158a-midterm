"""
iterate through each row of the data file to append relevant data to an OSC bundle
send the bundle of information through UDP socket and into the maxFile
"""

from __future__ import division
from OSC import OSCClient, OSCBundle
import csv
import time
import polylineMapper

def unpack(data, all_coords, socket):
    cX = all_coords[0]
    cY = all_coords[1]

    # client = OSCClient()
    # client.connect(("localhost", 15815))
    client = OSCClient()
    client.connect(("localhost", socket))

    """ prepare and send OSC bundles to Max from a list of tuples of coordinates """
    def bundle_polyline(coordinates, speed, polyline_type, lst, coordsX, coordsY):
        for pair in coordinates:

            # create an OSC bundle:
            bundle = OSCBundle()

            # append polyline_type: "trip" or "delay" (data for in between current and next trip)
            bundle.append({'addr': "/curr", 'args': [polyline_type]})

            # append min/max longX and latY to bundle:
            bundle.append({'addr': "/minX", 'args': [min(coordsX)]})
            bundle.append({'addr': "/maxX", 'args': [max(coordsX)]})
            bundle.append({'addr': "/minY", 'args': [min(coordsY)]})
            bundle.append({'addr': "/maxY", 'args': [max(coordsY)]})

            # append longX and latY to bundle
            bundle.append({'addr': "/longX", 'args': [pair[0]]})
            bundle.append({'addr': "/latY", 'args': [pair[1]]})
            
            # append start/end longX and latY of coordinates list
            x_vals = [coords[0] for coords in coordinates]
            bundle.append({'addr': "/startX", 'args': [x_vals[0]]})
            bundle.append({'addr': "/endX", 'args': [x_vals[len(x_vals) - 1]]})
            y_vals = [coords[1] for coords in coordinates]
            bundle.append({'addr': "/startY", 'args': [y_vals[0]]})
            bundle.append({'addr': "/endY", 'args': [y_vals[len(y_vals) - 1]]})

            # append speed
            bundle.append({'addr': "/speed", 'args': [speed]})

            # send bundle to Max:
            client.send(bundle)

            # delay time to even out polyline steps
            time.sleep(speed)

    for row in data:

        """ parse and set time stamps in minutes (i.e. 4:02 == 242) """
        pickup = row["pickuptime"].split(" ")[1]
        pickup = pickup.split(":")
        pickup = (int(pickup[0])*60) + int(pickup[1])

        dropoff = row["dropofftime"].split(" ")[1]
        dropoff = dropoff.split(":")
        dropoff = (int(dropoff[0])*60) + int(dropoff[1])

        next_pickup = row["nextpickuptime"].split(" ")[1]
        next_pickup = next_pickup.split(":")
        next_pickup = (int(next_pickup[0])*60) + int(next_pickup[1])  

        """ decode trippolyline """
        latlong_list = polylineMapper.decode(row["trippolyline"])
        latlong_speed = round((dropoff - pickup) / (2*len(latlong_list)), 10)  # translate 1 minute in RT == 0.5 seconds
        bundle_polyline(latlong_list, latlong_speed, "trip", latlong_list, cX, cY)

        """ decode nextpolyline """
        next_latlong = polylineMapper.decode(row["nextpolyline"])
        next_speed = round((next_pickup - dropoff) / (2*len(next_latlong)), 10)  # translate 1 minute in RT == 0.5 seconds
        bundle_polyline(next_latlong, next_speed, "delay", next_latlong, cX, cY)

    client.close()
