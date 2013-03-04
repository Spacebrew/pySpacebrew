#!/usr/bin/python
import time
import locale
import curses

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

stdscr = curses.initscr()
stdscr.keypad(1)
curses.noecho()			# turn off echo
curses.curs_set(0)		# turn off cursor

# create window for incoming and outgoing messages
outgoing = curses.newwin(50, 50, 0, 0)
confirm = curses.newwin(50, 20, 0, 55)
incoming = curses.newwin(50, 50, 0, 80)

outgoing.addstr("Client App Name: ", curses.A_BOLD)

try:
	counter = 0
	column_str = outgoing.getyx()[1]
	line = 0	
	message = ""

	while 1:
		c = stdscr.getch()
		counter += 1

		if len(message) > 30 or c == 10 or c == 13:

			if (c == 10 or c == 13) and len(message) > 0: 
				confirm.addstr(line, 0, " message sent       ", curses.A_STANDOUT)
				# TO COME: send messages to spacebrew
				message = ""	# reset message

			elif len(message) == 0:
				confirm.addstr(line, 0, " no message to send ", curses.A_STANDOUT)				

			else: 
				confirm.addstr(line, 0, " message too long   ", curses.A_STANDOUT)
				message = ""	# reset message

			line += 1
			counter = 0
			outgoing.addstr(line, 0, "Client App Name: ", curses.A_BOLD)

		elif c == curses.KEY_DC or c == curses.KEY_BACKSPACE or c == 127:
			message = message[0:-1]
			outgoing.addstr(line, (column_str + len(message)), " ")			


		else:
			message += chr(c)
			outgoing.addstr(line, column_str, message)
			column += 1

		confirm.refresh()
		outgoing.refresh()
		incoming.refresh()


# closing out the app and returning terminal to old settings
except (KeyboardInterrupt, SystemExit) as e:
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()