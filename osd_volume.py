#!/usr/bin/env python
# coding: utf8

#
# Little helper script to set the volume and toggle muting.
#
# 2014 - Philip Taffner <philip.taffner@bluegfx.de>
#

import sys, os, re
from subprocess import check_output, call

if len(sys.argv) < 2:
	print "Usage: %s <percentage(+|-)>|m"
	sys.exit(1)

if sys.argv[1] == "m":
	res = check_output("amixer -D pulse set Master toggle".split(" "))
	m = re.compile("\[(on|off)\]").search(res)
	status = "Muted" if m.group(1) == "off" else "Unmuted"

	os.system("killall osd_cat")
	os.system("echo %s | osd_cat -d 2 -A center -p middle -c lightblue -s 2 -f -adobe-helvetica-bold-r-*-*-34-*-*-*-*-*-*-*" % status)
else:
	res = check_output(("amixer set Master %s" % sys.argv[1]).split(" "))
	m = re.compile("\[(.+)%\]").search(res)

	if m:
		os.system("killall osd_cat")
		call(("osd_cat -d 2 -A center -p middle -c lightblue -b percentage -T Lautstärke -s 2 -f -adobe-helvetica-bold-r-*-*-34-*-*-*-*-*-*-* -P %s" % m.group(1)).split(" "))
	else:
		sys.stderr.write("Error: Could not read current volume level.\n")
		sys.exit(1)
