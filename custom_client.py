#!/usr/bin/python

import time
import locale
import curses
import random
from spacebrewInterface.spacebrew import Spacebrew

# set the encoding to use for the terminal string
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# initialize the terminal display
stdscr = curses.initscr()
stdscr.keypad(1)
curses.noecho()			# turn off echo
curses.curs_set(0)		# turn off cursor

# set-up a variables to hold coordinates
pos_state = 18
local_state = 0
remote_state = 0

# configure the spacebrew client
brew = Spacebrew("pyDice Example", server="sandbox.spacebrew.cc")
brew.addPublisher("roll of the dice", "dice")
brew.addSubscriber("what did you roll", "dice")

# function that handles the incoming spacebrew dice messages
def handleDice(value):
	global code, stdscr
	stdscr.addstr(pos_remote, pos_state, (" " * 30).encode(code))
	if value < 1 or value > 6:
		stdscr.addstr(pos_remote, pos_state, ("you rolled a " + str(value) + "! What kind of dice is that? ").encode(code))
	else: 
		stdscr.addstr(pos_remote, pos_state, str(value).encode(code))
	stdscr.refresh()

# register handler function with appropriate subscription data feed
brew.subscribe("what did you roll", handleDice)

try:
	# start-up spacebrew
	brew.start()	

	# create and load info message at the top of the terminal window
	info_msg = "This is the pySpacebrew library custom data type example. It rolls the dice every time the enter or return\n" 
	info_msg += "key is pressed (value between 0 and 6), and displays the latest dice roll value it has received.\n"  
	info_msg += "IMPORTANT: don't shrink the Terminal window as it may cause app to crash (bug with curses lib)."  
	stdscr.addstr(0, 0, info_msg.encode(code))
	stdscr.refresh()

	# update the location for the remote and local dice state 
	pos_local = stdscr.getyx()[0] + 2
	pos_remote = pos_local + 2

	# display the label for the remote and local dice roll states
	stdscr.addstr(pos_local, 0, "local dice roll: ".encode(code), curses.A_BOLD)
	stdscr.addstr(pos_remote, 0, "remote dice roll: ".encode(code), curses.A_BOLD)

	# display the starting prompt next to local and remote dice state lines
	stdscr.addstr(pos_local, pos_state, "waiting for first roll".encode(code))
	stdscr.addstr(pos_remote, pos_state, "waiting for first roll".encode(code))
	stdscr.refresh()

	# listen for keypresses and handle input
	while 1:
		c = stdscr.getch()

		if (c == 10 or c == 13): 
			local_state = random.randint(1,6)
			brew.publish("roll of the dice", local_state)
			stdscr.addstr(pos_local, pos_state, (" " * 30).encode(code))
			stdscr.addstr(pos_local, pos_state, str(local_state).encode(code))

		stdscr.refresh()

# closing out the app and returning terminal to old settings
finally:
	brew.stop()
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()
