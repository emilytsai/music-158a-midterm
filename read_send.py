from OSC import OSCClient, OSCBundle
import csv
import time

client = OSCClient()
client.connect(("localhost", 15815))

data = csv.DictReader(open('10RandomTrips.csv', 'rU'))
delay = 0
for row in data:
    ### Create a bundle:
    bundle = OSCBundle()
    # time stamps
    pickup = row["pickuptime"].split(" ")[1]
    pickup = pickup.split(":")
    pickup = (int(pickup[0])*100) + int(pickup[1])
    dropoff = row["dropofftime"].split(" ")[1]
    dropoff = dropoff.split(":")
    dropoff = (int(dropoff[0])*100) + int(dropoff[1])
    bundle.append({'addr': "/pickupTime", 'args': [pickup]})
    bundle.append({'addr': "/dropoffTime", 'args': [dropoff]})
    if delay != 0:
        time.sleep(pickup - delay)
    # pickup longX and latY
    bundle.append({'addr': "/pickupX", 'args': [float(row["pickupx"])]})
    bundle.append({'addr': "/pickupY", 'args': [float(row["pickupy"])]})
    # dropoff longX and latY
    bundle.append({'addr': "/dropoffX", 'args': [float(row["dropoffx"])]})
    bundle.append({'addr': "/dropoffY", 'args': [float(row["dropoffy"])]})
    ### Send bundle to Max:
    client.send(bundle)
    # time.sleep(1)
    time.sleep(dropoff - pickup)
    delay = dropoff