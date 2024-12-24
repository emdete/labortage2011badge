#!/bin/sh -e
echo "try to kill old instance: "
killall badge-tool || true
(
	(
		while true; do
			cat /proc/net/dev
			sleep 1
		done ) | awk '
BEGIN{m=0x0ffff;c=0}
/wlan0/{d1=($2-c1)/7; d2=($10-c2)/7; if (d1>m) d1=m; if (d2>m) d2=m; print "s", int(d1), int(d2), int(0); fflush(); c1=$2; c2=$10; }
	' | /home/mdt/Source/oss/labortage2011badge/commandline/badge-tool -i -
) &
