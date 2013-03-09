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

# configure the spacebrew client
brew = SpaceBrew("pyString Example", server="sandbox.spacebrew.cc")
brew.addPublisher("send msg", "string")
brew.addSubscriber("get_msg", "string")

def handleString(value):
	global pos, code, stdscr
	stdscr.addstr(pos["y"], 0, "incoming: ".encode(code), curses.A_BOLD)
	stdscr.addstr(pos["y"], pos["x"] + pos_msg, value.encode(code))
	stdscr.refresh()
	pos["y"] += 1

brew.subscribe("get_msg", handleString)

# set-up a variables to hold coordinates
pos = { "x":0, "y":0 }
pos_in = 0
pos_msg = 10
pos_max = 60
pos_con = pos_msg + pos_max + 5

try:
	brew.start()

	info_msg = "This is the pySpacebrew library string example. It functions like a chat program. You can\n" 
	info_msg += "send messages up 60 char long. Only the first 60 chars of incoming messages will be displayed."  

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
			brew.publish('send msg',cur_line)
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
