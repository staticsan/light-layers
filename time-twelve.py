
import lightlayers
l = lightlayers.LightLayer(True, '10.10.10.44')

l.ramp(0, 12, 500, 0)
delay = 50

for x in range(0, 3):
	l.setblock(8, 11, "black")
	l.setblock(0, 3, "green")
	l.wait(delay)

	l.setblock(0, 3, "black")
	l.setblock(4, 7, "teal")
	l.wait(delay)

	l.setblock(4, 7, "black")
	l.setblock(8, 11, "darkred")
	l.wait(delay)

l.setblock(8, 11, "black")
# l.ramp(0, 12, 500, 0)
l.wait(10)
l.render()
