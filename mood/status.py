#!/usr/bin/env -S python3 -u
from pathlib import Path
from time import sleep
from LaborBadge import LaborBadge


def main():
	f=LaborBadge()
	r = g = b = 0
	vol = 0
	while True:
		lines = Path("/proc/net/dev").read_text().splitlines()
		lines = [line.split() for line in lines if "wlan0" in line]
		lines = (int(lines[0][1]) + int(lines[0][9])) // 1024
		r = min((lines-vol)*30, 0xffff)
		vol = lines
		lines = Path("/proc/loadavg").read_text().splitlines()
		lines = [line.split() for line in lines]
		b = int(float(lines[0][0]) * 5000)
		print(r, g, b)
		f.setColor(r, g, b)
		sleep(.5)

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])
# vim:tw=0:nowrap
