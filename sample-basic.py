"""Simple Sample program for light-layers."""

import lightlayers

# Change this to your Holiday's address. This is one of mine.
l = lightlayers.LightLayer(True, '10.10.10.44')

# Set up a brightness ramp on lights 10 thru 40, 500 milliseconds raise, 70% overlap.
l.ramp(10, 40, 500, 70)
# Paint a gradient from lights 10 to 20
l.gradient(10, 20, [0, 0xff, 0], [0, 0, 0xff])
# Paint another gradient for lights 21 to 40
l.gradient(21, 40, [0, 0, 0xff], [0xff, 0, 0])
# Move "here" to the furthest mapped extent 
l.wait()
# Ramp them down again
l.ramp(10, 40, 500, 70, "down")
l.wait()

# Send it out! There is a timing issue at the moment, so this is not as fast as it quite should be.
l.render()

