This requires use of the websocket-client library ... https://github.com/liris/websocket-client

It can be installed using 'pip install websocket-client'

Be aware that there is another python package called 'websocket' that uses the same package name. If you have websocket installed you will need to uninstall it before installing websocket-client. (You can uninstall if with 'pip uninstall websocket'.)

The other libraries should be standard. The first example simply posts a message every 5 seconds and prints incoming messages. It's as reduced as made sense to me, but could use a lot of work, particularly around parsing the incoming messages in meaningful ways.

