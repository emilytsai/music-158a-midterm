"""
Takes in command line inputs and sets up CSV readers. Starts the program.
"""

import sys
import csv
import multiprocessing
import datasend
import coordinates

files = []
coordsList = []

if len(sys.argv) < 2 or len(sys.argv) > 5:
        sys.exit("ERROR: Incorrect number of arguments. Please run 'python run.py arg1 *arg2 *arg3 *arg4' where arg2-arg4 are optional arguments.")
else:
    for x in range(len(sys.argv) - 1):
        data = csv.DictReader(open(sys.argv[x + 1], 'rU'))
        coords = coordinates.get(data)
        coordsList += [coords]
        data = csv.DictReader(open(sys.argv[x + 1], 'rU'))
        files += [data]

datafiles = {'data' : files, 'coords' : coordsList}

def startProgram():
    socket = 15800
    if __name__ == "__main__":
        for x in range(len(datafiles['data'])):
            p = multiprocessing.Process(target=datasend.unpack, args=(datafiles['data'][x], datafiles['coords'][x], socket))
            p.start()
            socket += 1

startProgram()
