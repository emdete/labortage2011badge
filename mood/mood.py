#!/usr/bin/env python3
from math import floor
from os import system
from time import sleep
from LaborBadge import LaborBadge

def hsv2rgb(h, s, v):
	' calculate rgb from hsv values '
	h = float(h)
	s = float(s)
	v = float(v)
	h60 = h / 60.0
	h60f = floor(h60)
	hi = int(h60f) % 6
	f = h60 - h60f
	p = v * (1 - s)
	q = v * (1 - f * s)
	t = v * (1 - (1 - f) * s)
	r, g, b = 0, 0, 0
	if hi == 0: r, g, b = v, t, p
	elif hi == 1: r, g, b = q, v, p
	elif hi == 2: r, g, b = p, v, t
	elif hi == 3: r, g, b = p, q, v
	elif hi == 4: r, g, b = t, p, v
	elif hi == 5: r, g, b = v, p, q
	r, g, b = int(r * 0xffff), int(g * 0xffff), int(b * 0xffff)
	return r, g, b

def main():
	while False:
		for key in range(0, 360, 5):
			print('../commandline/badge-tool -s {}:{}:{}'.format(*hsv2rgb(key, 1, 1)))
			system('../commandline/badge-tool -s {}:{}:{}'.format(*hsv2rgb(key, 1, 1)))
			sleep(.1)
	color = 300
	count = 200
	with LaborBadge() as f:
		while False:
			for key in range(0, 360, 3):
				f.setColor(*hsv2rgb(key, 1, 1))
				sleep(.03)
		print("temperature=", f.getTemprature())
		print("color=", f.getColor())
		print("getButton", f.getButton())
		f.setColor(0, 0, 0)
		o = 0
		while True:
			for b in range(1, 8):
				if f.getButton(): break
				x = [a+b for a,b in zip(
					[-color * (o >> i & 1) for i in range(3)],
					[color * (b >> i & 1) for i in range(3)],
					)]
				f.fadeDelta(count, *x)
				sleep(count / 125)
				o = b
			f.setColor(count*color, count*color, count*color)
			sleep(count / 125)


if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])
# vim:tw=0:nowrap
