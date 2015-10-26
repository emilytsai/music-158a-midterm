"""
sets up csv readers and starts the program
"""

import sys
import csv
import multiprocessing
import readSend
import getCoords

files = []
coordinates = []
if len(sys.argv) < 2 or len(sys.argv) > 5:
        sys.exit("ERROR: incorrect number of arguments. please run 'python run.py arg1 *arg2 *arg3 *arg4' where arg2-arg4 are optional arguments.")
else:
    for x in range(len(sys.argv) - 1):
        data = csv.DictReader(open(sys.argv[x + 1], 'rU'))
        coords = getCoords.get(data)
        coordinates += [coords]
        data = csv.DictReader(open(sys.argv[x + 1], 'rU'))
        files += [data]

datafiles = {'data' : files, 'coords' : coordinates}

def startProgram():
    socket = 15800
    if __name__ == "__main__":
        for x in range(len(datafiles['data'])):
            p = multiprocessing.Process(target=readSend.unpack, args=(datafiles['data'][x], datafiles['coords'][x], socket))
            p.start()
            socket += 1

startProgram()
