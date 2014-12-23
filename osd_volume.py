#!/usr/bin/env python
# coding: utf8

#
# Little helper script to set the volume and toggle muting.
#
# 2014 - Philip Taffner <philip.taffner@bluegfx.de>
#

import sys, os, re, pynotify
from subprocess import check_output, call

def toggleMute():
	res = check_output("amixer -D pulse set Master toggle".split(" "))
	m = re.compile("\[(on|off)\]").search(res)

	if m.group(1) == "on":
		setVolume("0+")
		return

	os.system("killall notify-osd");
	if not pynotify.init("osd_volume"):
		sys.exit(1)

	n = pynotify.Notification("Lautstärke", "", "audio-volume-muted")
	n.set_hint("x-canonical-private-synchronous", "")
	n.set_hint_int32("value", 0)

	if not n.show():
		print "Failed to send notification"
		sys.exit(1)

def setVolume(value):
	res = check_output(("amixer set Master %s" % value).split(" "))
	m = re.compile("\[(.+)%\]").search(res)

	if m:
		os.system("killall notify-osd");
		if not pynotify.init("osd_volume"):
			sys.exit(1)

		n = pynotify.Notification("Lautstärke", "", "audio-volume-high")
		n.set_timeout(pynotify.EXPIRES_DEFAULT)
		n.set_hint("x-canonical-private-synchronous", "")
		n.set_hint_int32("value", int(m.group(1)))

		if not n.show():
			print "Failed to send notification"
			sys.exit(1)
	else:
		sys.stderr.write("Error: Could not read current volume level.\n")
		sys.exit(1)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: %s <percentage(+|-)>|m"
		sys.exit(1)

	if sys.argv[1] == "m":
		toggleMute()
	else:
		setVolume(sys.argv[1])
