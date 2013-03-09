#!/usr/bin/python

import time
import locale
import curses
from spacebrewInterface.spacebrew import SpaceBrew

# set the encoding to use for the terminal string
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# initialize the terminal display
stdscr = curses.initscr()
stdscr.keypad(1)
curses.noecho()			# turn off echo
curses.curs_set(0)		# turn off cursor

# set-up a variables to hold coordinates
pos = { "x":0, "y":0 }
pos_state = 15
local_state = False
remote_state = False

# configure the spacebrew client
brew = SpaceBrew("pyBoolean Example", server="sandbox.spacebrew.cc")
brew.addPublisher("local state", "boolean")
brew.addSubscriber("remote state", "boolean")

def handleBoolean(value):
	global pos, code, stdscr
	stdscr.addstr(pos_remote, pos_state, (str(value) + "  ").encode(code))
	stdscr.refresh()

brew.subscribe("remote state", handleBoolean)

try:
	brew.start()

	info_msg = "This is the pySpacebrew library boolean example. It sends out a boolean message every time\n" 
	info_msg += "the enter or return key is pressed, and it also displays receives a remote boolean value."  

	stdscr.addstr(pos["y"], pos["x"], info_msg.encode(code))
	stdscr.refresh()

	pos_local = stdscr.getyx()[0] + 2
	pos_remote = pos_local + 1
	stdscr.addstr(pos_local, 0, "local state: ".encode(code), curses.A_BOLD)
	stdscr.addstr(pos_local, pos_state, (str(local_state) + "  ").encode(code))
	stdscr.addstr(pos_remote, 0, "remote state: ".encode(code), curses.A_BOLD)
	stdscr.addstr(pos_remote, pos_state, (str(remote_state) + "  ").encode(code))
	stdscr.refresh()

	column_str = stdscr.getyx()[1]
	cur_line = ""

	while 1:
		c = stdscr.getch()

		if (c == 10 or c == 13): 
			local_state = not local_state
			brew.publish('local state', local_state)
			stdscr.addstr(pos_local, pos_state, (str(local_state) + "  ").encode(code))

		stdscr.refresh()

# closing out the app and returning terminal to old settings
finally:
	brew.stop()
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()
