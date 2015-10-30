"""
Reset and close all UDP sockets to silence any remaining sounds in Max.
"""

from OSC import OSCClient, OSCBundle

socket = 15800

for x in range(4):
    client = OSCClient()
    client.connect(("localhost", socket))
    bundle = OSCBundle()

    bundle.append({'addr': "/curr", 'args': [" "]})

    bundle.append({'addr': "/minX", 'args': [0]})
    bundle.append({'addr': "/maxX", 'args': [0]})
    bundle.append({'addr': "/minY", 'args': [0]})
    bundle.append({'addr': "/maxY", 'args': [0]})

    bundle.append({'addr': "/longX", 'args': [0]})
    bundle.append({'addr': "/latY", 'args': [0]})
    
    bundle.append({'addr': "/startX", 'args': [0]})
    bundle.append({'addr': "/endX", 'args': [0]})
    bundle.append({'addr': "/startY", 'args': [0]})
    bundle.append({'addr': "/endY", 'args': [0]})

    bundle.append({'addr': "/passengers", 'args': [0]})

    client.send(bundle)
    client.close()
    socket += 1
