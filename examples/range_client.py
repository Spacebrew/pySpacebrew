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

# get app name and server from query string
name = "pyRange Example"
server = "sandbox.spacebrew.cc"

for cur_ele in sys.argv:
	if "name" in cur_ele: 
		name = cur_ele[5:]
	if "server" in cur_ele: 
		server = cur_ele[7:]

# configure the spacebrew client
brew = Spacebrew(name, server=server)
brew.addPublisher("slider", "range")
brew.addSubscriber("graph", "range")

# set-up a variables to hold coordinates
pos_state = 21
pos_int = 15
col_local = 0
col_remote = 0

# set-up a variables to hold state
local_state = 500
remote_state = 0

# method that updates the range "bars" and value on the display
def displayRange(value, source_line):
	remote_state = value
	stdscr.addstr(source_line, pos_int, "     ".encode(code))
	stdscr.addstr(source_line, pos_int, str(value).encode(code))
	stdscr.addstr(source_line, pos_state, "".encode(code))
	for i in range(100):
		if (value / 10) > i:
			stdscr.addstr(" ".encode(code), curses.A_STANDOUT)
		else: 
			stdscr.addstr(" ".encode(code))
	stdscr.refresh()

# function that handles the incoming spacebrew range messages
def handleRange(value):
	global code, stdscr
	remote_state = value
	displayRange(remote_state, col_remote)

# registering range handler method with appropriate subscription feed
brew.subscribe("graph", handleRange)

try:
	brew.start()

	# set app information message
	info_msg =  "This is the pySpacebrew library range example. This app sends out a range value, between 0 and 1023. The value \n"
	info_msg += "increases and decreases in response to '+'/'=' and `-`/'_' key presses. App also displays a range value received\n"  
	info_msg += "from Spacebrew. Connected as: " + name + "\n"
	info_msg += "IMPORTANT: don't shrink the Terminal window as it may cause app to crash (bug with curses lib)."  
	stdscr.addstr(0, 0, info_msg.encode(code))
	stdscr.refresh()

	# update the location of the local and remote range linds
	col_local = stdscr.getyx()[0] + 2
	col_remote = col_local + 2

	# display the label for the remote and local range states
	stdscr.addstr(col_local, 0, "local range:  ".encode(code), curses.A_BOLD)
	stdscr.addstr(col_remote, 0, "remote range: ".encode(code), curses.A_BOLD)

	# display the starting state for remote and local range states
	displayRange(local_state, col_local) 	
	displayRange(remote_state, col_remote) 
	stdscr.refresh()

	# listen for keypresses and handle input
	while 1:
		c = stdscr.getch()

		new_data = False
		if c == ord('+') or c == ord('='):
			local_state += 10
			if local_state > 1023: local_state = 1023
			new_data = True
		elif c == ord('-') or c == ord('_'):
			local_state -= 10
			if local_state < 0: local_state = 0
			new_data = True

		if new_data:
			brew.publish("slider", local_state)
			displayRange(local_state, col_local)

		stdscr.refresh()

# closing out the app and returning terminal to old settings
finally:
	brew.stop()
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()
