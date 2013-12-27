
import lightlayers
l = lightlayers.LightLayer(True, '10.10.10.44')

l.ramp(0, 12, 500, 0)
delay = 50

l.setblock(0, 1, "blue")
l.wait(delay)
l.setblock(0, 1, "black")
l.wait(delay)
l.setblock(0, 1, "blue")
l.wait(delay)
l.setblock(0, 1, "black")
l.wait(delay)
l.setblock(0, 1, "blue")
l.wait(delay)
l.setblock(0, 1, "black")
l.wait(delay)

l.render_rest()

