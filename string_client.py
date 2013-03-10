#!/usr/bin/python

import time
import locale
import curses
from spacebrewInterface.spacebrew import Spacebrew

# set the encoding to use for the terminal string
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# initialize the terminal display
stdscr = curses.initscr()
stdscr.keypad(1)
curses.noecho()			# turn off echo
curses.curs_set(0)		# turn off cursor

# configure the spacebrew client
brew = Spacebrew("pyString Example", server="sandbox.spacebrew.cc")
brew.addPublisher("chat outgoing", "string")
brew.addSubscriber("chat incoming", "string")

def handleString(value):
	global pos, code, stdscr
	stdscr.addstr(pos["y"], 0, "incoming: ".encode(code), curses.A_BOLD)
	stdscr.addstr(pos["y"], pos["x"] + pos_msg, value.encode(code))
	stdscr.refresh()
	pos["y"] += 1

brew.subscribe("chat incoming", handleString)

# set-up a variables to hold coordinates
pos = { "x":0, "y":0 }
pos_in = 0
pos_msg = 10
pos_max = 60
pos_con = pos_msg + pos_max + 5

try:
	brew.start()

	info_msg = "This is the pySpacebrew library string example. It functions like a chat program. It can\n"
	info_msg += "send messages up 60 char long and it displays the first 60 chars of incoming messages.\n"  
	info_msg += "IMPORTANT: don't shrink the Terminal window as it may cause app to crash (bug with curses lib)."  

	stdscr.addstr(pos["y"], pos["x"], info_msg.encode(code))
	stdscr.refresh()

	pos_in = stdscr.getyx()[0] + 2
	pos["y"] = pos_in + 2
	stdscr.addstr(pos_in, 0, "new msg: ".encode(code), curses.A_BOLD)
	stdscr.refresh()

	column_str = stdscr.getyx()[1]
	cur_line = ""

	while 1:
		c = stdscr.getch()

		if (c == 10 or c == 13) and len(cur_line) > 0: 
			brew.publish('chat outgoing',cur_line)
			stdscr.addstr(pos_in, pos_con, " cur_line sent      ".encode(code), curses.A_STANDOUT)
			stdscr.addstr(pos["y"], 0, "outgoing: ".encode(code), curses.A_BOLD)
			stdscr.addstr(pos["y"], pos_msg, cur_line.encode(code))
			cur_line = ""
			stdscr.addstr(pos_in, pos_msg, (" " * pos_max).encode(code))			
			pos["y"] += 1

		elif (c == 10 or c == 13) and len(cur_line) == 0:
			stdscr.addstr(pos_in, pos_con, " no message to send ".encode(code), curses.A_STANDOUT)			

		elif c == curses.KEY_DC or c == curses.KEY_BACKSPACE or c == 127:
			cur_line = cur_line[0:-1]
			stdscr.addstr(pos_in, (pos["x"] + pos_msg + len(cur_line)), " ".encode(code))			
			stdscr.addstr(pos_in, pos_con, "                     ".encode(code))

		elif len(cur_line) >= (pos_max): 
			stdscr.addstr(pos_in, pos_con, " your at my limit   ".encode(code), curses.A_STANDOUT)

		elif c < 256 and c > 0:
			cur_line += chr(c)
			stdscr.addstr(pos_in, pos["x"] + pos_msg, cur_line.encode(code))
			stdscr.addstr(pos_in, pos_con, "                     ".encode(code))

		stdscr.refresh()

# closing out the app and returning terminal to old settings
finally:
	brew.stop()
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()
