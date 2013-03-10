pySpacebrew - Spacebrew Python Library and Core Examples  
---------------------------------------------------------  
  
This repo contains the Spacebrew Library for Python along with documentation and example apps. Below is a brief overview about Spacbrew, followed by a short tutorial on how to use this library.  
  
Current Version: 1.0.1  
Latest Update: March 9, 2013   
Developed By: contributed by Adam Mayer, maintained by Julio Terra (LAB at Rockwell Group)   
  
Jump to:  
* [Using the pySpacebrew Library](#using-library)  
* [pySpacebrew Example Appss](#example-apps)  
  
About Spacebrew  
===============  
Spacebrew is an open, dynamically re-routable software toolkit for choreographing interactive spaces. Or, in other words, a simple way to connect interactive things to one another. Every element you hook up to the system can subscribe to, and publish data feeds. Each data feed has a data type. There are three different data types supported by Spacebrew: boolean (true/false), number range (0-1023) or string (text). Once elements are set up, you can use a web based visual switchboard to connect or disconnect publishers and subscribers to each other.  
  
[Learn more about Spacebrew here.](http://docs.spacebrew.cc/)  
  
Using Library
==============   
  
###Before you Get Started: Install Dependencies   
Before you get started you need to install the appropriate websockets library. There are many different ones out there, so make sure to get the one called `websocket-client`. [Here is a link to code repo for the `websocket-client` library](https://github.com/liris/websocket-client). The easiest way to install this library is using pip, python's package manager. If you have pip installed on your computer all you have to do is run the command below in the Terminal (or whichever other console app you prefer). Otherwise, follow the instructions on the `websocket-client` repo.  
  
```
pip install websocket-client
```
  
If you have the wrong websocket library installed you will need to uninstall it before installing websocket-client. Using pip, you can uninstall if by running the following command `pip uninstall websocket`.  
  
###1. Import python library into your project  
Import the Spacebrew class into your project using a `from ... import` command at the start of your script. Please note that if you change the name of the folder or file containing the Spacebrew class then you will need to update the sample command below accordingly.  
  
```
from spacebrewInterface.spacebrew import Spacebrew
```
   
###2. Create a Spacebrew object  
Create an instance of a Spacebrew Client object using the `Spacebrew` class constructor.  

Syntax Overview:
```
brew = Spacebrew("app name", description="app description", server="sandbox.spacebrew.cc", port=9000):
```

Example From String_Client.py App
```
brew = Spacebrew("pyString Example", server="sandbox.spacebrew.cc")
```
  
**Constructor Parameters**
The constructor accepts four parameters: `name`, `server`, `description`, and `port`. The last three of these are optional. If server is not specified then it will default to `sandbox.spacebrew.cc`, the description will default to an empty string, while the port will default to 9000.  
         
###3. Configure data subscription and publication Feeds  
The next step involves specifying the subscription and publication data feeds. Each data feed needs to be assigned a unique label and a data type. The standard data types are: `"string"`, `"range"`, of `"boolean"`. Custom data types are also supported. The name of a custom data type is arbitrary. To link custom publication and subscription data feeds the name needs to be consistent accross both.   

Syntax Overview:
```
brew.addPublisher("publish feed name", "data type")
brew.addSubscriber("subscribe feed name", "data type")
```

Example From String_Client.py App
```
brew.addPublisher("local state", "boolean")
brew.addSubscriber("remote state", "boolean")
```
  
###4. Define message event handler methods
Once you've defined the subscription data feeds you need to configure the callback methods that will handle messages received via Spacebrew. This step is crucial to enable your app to respond to Spacebrew messages


Syntax Overview:
```
def handlerMethod(value):
	# do something with the value received

brew.subscribe("subscribe feed name", handlerMethod)
```

Example From String_Client.py App  
```
def handleBoolean(value):
	global pos, code, stdscr
	stdscr.addstr(pos_remote, pos_state, (str(value) + "  ").encode(code))
	stdscr.refresh()

brew.subscribe("remote state", handleBoolean)
```
  
The current version of the python library does not offer hooks for lifecycle events such as on open, on close and on error. However, it does output messages to the terminal the confirme when the Spacebrew connection is opened and closed. This is a feature that will be added in a future update.

###6. Connect to Spacebrew
Now that you have configured the Spacebrew object it is time to connect to the Spacebrew server. 
  
```
brew.start()
```
  
###7. Publish messages  
The `publish` method enables you to publish messages via one of the publication data feeds. It accepts two mandatory parameters, a channel name and a value. The value needs to correspond to the expected data type otherwise the message will be ignored by the server.  
    
```
brew.publish("publish feed name","data")
```

Example Apps
=============

Here is a list of the core examples that are included in this repo. These examples were designed to help you get started building apps that connect to other applications, objects and spaces via Spacebrew. Please note that all of these apps run in the terminal and use python's standard curse library to handle the UI.

###Boolean Client
App that sends out a boolean message every time the enter or return key is pressed, and displays the latest boolean value it has received.

###String Client
App that functions like a chat program. It can send messages up 60 char long and it displays the first 60 chars of incoming messages.

###Range Client
App that sends out a range value (0 - 1023). The value increases and decreased in response to `+` and `-` keys. App also displays a range value received from Spacebrew.
  
###Custom Client (Virtual Dice App)
App that publishes and subscribes to a custom data type called dice. It rolls a virtual dice every time the enter or return key is pressed (generates a random number between 1 and 6). It also displays the latest remote dice roll value received.

  
License  
=======  
  
The MIT License (MIT)  
Copyright © 2012 LAB at Rockwell Group, http://www.rockwellgroup.com/lab  
  
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  
  
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  
  
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.  

