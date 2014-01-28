#!/usr/bin/python

import time
import locale
import curses
import sys
from pySpacebrew.spacebrew import Spacebrew

# set the encoding to use for the terminal string
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# initialize the terminal display
stdscr = curses.initscr()
stdscr.keypad(1)
curses.noecho()			# turn off echo
curses.curs_set(0)		# turn off cursor

# set-up a variables to hold coordinates
pos_state = 15
local_state = False
remote_state = False

# get app name and server from query string
name = "pyBoolean Example"
server = "sandbox.spacebrew.cc"

for cur_ele in sys.argv:
	if "name" in cur_ele: 
		name = cur_ele[5:]
	if "server" in cur_ele: 
		server = cur_ele[7:]


# configure the spacebrew client
brew = Spacebrew(name=name, server=server)
brew.addPublisher("local state", "boolean")
brew.addSubscriber("remote state", "boolean")

def handleBoolean(value):
	global code, stdscr
	stdscr.addstr(pos_remote, pos_state, (str(value) + "  ").encode(code))
	stdscr.refresh()

brew.subscribe("remote state", handleBoolean)

try:
	# start-up spacebrew
	brew.start()

	# create and load info message at the top of the terminal window
	info_msg = "This is the pySpacebrew library boolean example. It sends out a boolean message every time\n" 
	info_msg += "the enter or return key is pressed and displays the latest boolean value it has received.\n"  
	info_msg += "Connected to Spacebrew as: " + name + "\n"
	info_msg += "IMPORTANT: don't shrink the Terminal window as it may cause app to crash (bug with curses lib)."  
	stdscr.addstr(0, 0, info_msg.encode(code))
	stdscr.refresh()

	# update the location for the remote and local dice state 
	pos_local = stdscr.getyx()[0] + 2
	pos_remote = pos_local + 2

	# display the label for the remote and local boolean states
	stdscr.addstr(pos_local, 0, "local state: ".encode(code), curses.A_BOLD)
	stdscr.addstr(pos_remote, 0, "remote state: ".encode(code), curses.A_BOLD)

	# display the starting state for remote and local boolean states
	stdscr.addstr(pos_local, pos_state, (str(local_state) + "  ").encode(code))
	stdscr.addstr(pos_remote, pos_state, (str(remote_state) + "  ").encode(code))
	stdscr.refresh()

	# listen for keypresses and handle input
	while 1:
		c = stdscr.getch()

		if (c == 10 or c == 13): 
			local_state = not local_state
			brew.publish('local state', str(local_state).lower())
			stdscr.addstr(pos_local, pos_state, (str(local_state) + "  ").encode(code))

		stdscr.refresh()

# closing out the app and returning terminal to old settings
finally:
	brew.stop()
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()
