#!/usr/bin/python
#
"""
LightLayers module for Holiday by Moorescloud

Copyright (c) 2013, Wade Bowmer
License: ..
"""

__author__ = 'Wade Bowmer'
__version__ = '0.01-dev'
__license__ = 'MIT'

import time
import colours

class LightLayer:

	remote = False
	addr = ''
	NUM_GLOBES = 50
	stream = { }
	current_time = 0
	furthest_edge = 0
	time_step = 50 # milli-seconds
	stream = { }

	def __init__(self, remote=False, addr=''):
		"""Remote mode only, at the moment."""
		if remote:
			self.remote = True
			self.addr = addr
		self.stream[self.current_time] = [ [0, 0, 0, 0] for g in range(self.NUM_GLOBES) ] # red green blue transparency
	
	def setcolour(self, col):
		"""Generic colour checks. Also does a lookup if you've provided a name."""
		if type(col) is list and len(col) == 3:
			return [ self.limit(col[i], 0, 0xff) for i in [0, 1, 2] ]
		if type(col) is str:
			col = col.lower().replace(' ','')
			if col in colours.colourMap:
				return list(colours.colourMap[col])
		return False
	
	def limit(self, value, bottom, top):
		"""Helper function to range limit values."""
		return max(bottom, min(value, top))
	
	def setglobe(self, globe, col, trans=100):
		"""Set a single globe"""
		self.setblock(globe, globe, col, trans)

	def setblock(self, globe_start, globe_end, col, trans=100):
		"""Set a range of lights to the same colour. If you want to _not_ set the transparancy, use gradient()."""
		col = self.setcolour(col)
		if col:
			col.append(self.limit(trans, 0, 100))
			globe_start = self.limit(globe_start, 0, self.NUM_GLOBES-1)
			globe_end = self.limit(globe_end, 0, self.NUM_GLOBES-1)
			for g in range(globe_start, glob_end):
				self.stream[self.current_time][g] = list(col)

	def ramp(self, globe_start, globe_end, first_time, overlap=100, mode="up"): # aka raise
		"""Set an increasing brightness/transparency ramp
		This call does NOT set colour.
		first_time is how long the first light will take in milliseconds
		overlap is the percentage overlap subsequent lights will take. Overlap of 100 will bring them all up at once.
		"""
		globe_start = self.limit(globe_start, 0, self.NUM_GLOBES-1)
		globe_end = self.limit(globe_end, 0, self.NUM_GLOBES-1)
		overlap = self.limit(overlap, 0, 100)

		if first_time == 0:
			for g in range(globe_start, globe_end+1):
				self.stream[current_time][g][3] = 100
		else:
			time_advance = first_time
			time_overlap = int(time_advance * (100 - overlap)/100 / self.time_step) * self.time_step
			gtime = self.current_time
			first_time = float(first_time)
			for g in range(globe_start, globe_end+1):
				# print "Setting %d from %d" % (g, gtime)
				self.fill_to(gtime + time_advance)
				t = gtime
				while t <= gtime + time_advance:
					# print "Setting %f:%d to %f" % (t, g, (t - gtime) / first_time)
					if mode == "down":
						self.stream[t][g][3] = int(100 - (t - gtime) / first_time * 100)
					else:
						self.stream[t][g][3] = int((t - gtime) / first_time * 100)
					t += self.time_step
				gtime = gtime + time_overlap
		return

	def gradient(self, globe_start, globe_end, colour_from, colour_to):
		"""Set a gradient across a section of lights.
		"""
		globe_start = self.limit(globe_start, 0, self.NUM_GLOBES-1)
		globe_end = self.limit(globe_end, 0, self.NUM_GLOBES-1)
		span = globe_end - globe_start
		colour_from = self.setcolour(colour_from)
		colour_to = self.setcolour(colour_to)

		here = self.current_time + 0
		g = globe_start
		while g <= globe_end:
			factor = (g - globe_start)*100 / span 
			unfactor = float(100 - factor) / 100
			factor = float(factor) / 100
			# print "Wash of %f:%f" % (factor, unfactor)
			self.stream[here][g] = [
				int(colour_from[0] * unfactor + colour_to[0] * factor),
				int(colour_from[1] * unfactor + colour_to[1] * factor),
				int(colour_from[2] * unfactor + colour_to[2] * factor),
				self.stream[self.current_time][g][3] ]
			t = here
			while t <= self.furthest_edge:
				self.stream[t][g] = [ self.stream[here][g][0], self.stream[here][g][1], self.stream[here][g][2], self.stream[t][g][3] ]
				t += self.time_step
			g += 1

	def wash(self, globe_start, globe_end, steps, delay, start_from, colour_list):
		"""Set a moving gradient."""
		globe_start = self.limit(globe_start, 0, self.NUM_GLOBES-1)
		globe_end = self.limit(globe_end, 0, self.NUM_GLOBES-1)
		if delay < 0:
			delay = 0

		# Setup the raw colours
		colours = [ ]
		c = self.setcolour(colour_list.pop())
		while c and len(colour_list) > 1:
			d = max(0, colour_list.pop())
			from_c = c
			c = self.setcolour(colour_list)
			if c:
				x = 0
				while x < d:
					factor = (x - d)*100 / d
					unfactor = float(100 - factor)/100
					factor = float(factor)/100
					colours.append( [
						int(from_c[0] * unfactor + c[0] * factor),
						int(from_c[1] * unfactor + c[1] * factor),
						int(from_c[2] * unfactor + c[2] * factor) ])
					x += 1
		if c:
			colours.append(c)	

		# Now paint them 
		span = globe_end - globe_start
		here = self.current_time + 0
		self.fill_to(here + steps * delay)
		inner_step = delay
		while steps > 0:
			c = start_from
			for g in range(globe_start, globe_end+1):
				self.stream[here][g] = [ colours[c][0], colours[c][1], colours[c][2], self.stream[here][g][3] ]
				c += 1
			inner_step -= self.time_step
			if inner_step <= 0:
				inner_step = delay
				steps -= 1
				start_from += 1
			here += self.time_step


	def rotate(self, globe_start, globe_end, steps, distance, delay):
		"""Rotate the colours of a subset of globes."""
		globe_start = self.limit(globe_start, 0, self.NUM_GLOBES-1)
		globe_end = self.limit(globe_end, 0, self.NUM_GLOBES-1)
		span = globe_end - globe_start
		if delay < 0:
			delay = 0
		if distance == 0:
			return # whoops nothing to do!

		colours = []
		for g in range(globe_start, globe_end+1):
			colours.append([ self.stream[self.current_time][g][0], self.stream[self.current_time][g][1], self.stream[self.current_time][g][2] ])
		self.fill_to(self.current_time + steps * delay)
		# while steps > 0:

	# def shift(self, 

	def wait(self, delay=False):
		"""Move the "current" time forward by this amount in milliseconds.
		Called without an argument will move 'now' to the latest that's been recorded.
		"""
		if delay == False:
			self.current_time = self.furthest_edge
		else:
			distance = self.current_time + delay
			self.fill_to(distance)
			self.current_time = distance

	def fill_to(self, target):
		"""Extends the light storage forward in time, copying the most-recent values.
		Calling with a target before the furthest extent will do nothing.
		"""
		here = self.furthest_edge
		# print "Filling %d to %d" % (here, target)
		current_globes = self.stream[here]

		self.furthest_edge += self.time_step
		while self.furthest_edge <= target:
			self.stream[self.furthest_edge] = [ current_globes[g][:] for g in range(self.NUM_GLOBES) ]
			self.furthest_edge += self.time_step
		self.furthest_edge -= self.time_step
		return

	def go(self):
		"""This is intended for debugging."""
		t = 0
		times = self.stream.keys()
		times.sort()
		for t in times:
			print "%d: " % t,
			for g in self.stream[t]:
				if g[3] > 0:
					print '%02x%02x%02x_%d' % (g[0], g[1], g[2], g[3]),
				else:
					print '-',
			print

	def render(self):
		"""Renders the output to a Holiday device.
		Local rendering is currently not supported.
		"""
		t = 0
		delay = float(self.time_step) / 1000 / 2

		if (self.remote == True):
			import requests, json

			while t < self.current_time:
				globes = []
				for c in self.stream[t]:
					if c[3] == 100:
						globes.append("#%02x%02x%02x" % (c[0], c[1], c[2]))
					else:
						globes.append("#%02x%02x%02x" % (c[0] * c[3]/100, c[1] * c[3]/100, c[2] * c[3]/100))
				message = json.dumps({ "lights": globes })
				r = requests.put('http://%s/iotas/0.1/device/moorescloud.holiday/localhost/setlights' % self.addr, data=message)
				time.sleep(delay)
				t += self.time_step
		else:
			self.go()


if __name__ == '__main__':
	layer = LightLayer(remote=False)
	print layer

