************************************************
 ABOUT 
************************************************
* App: spacebrew-python-examples
* Team: labatrockwell, phooky (github)
 
Description:
* This project is a set of tools and examples for interfacing to SpaceBrew through python code.  
* The spacebrewInterface is a python API that allows easy communication with SpaceBrew.  
* The spacebrewLink is a dynamic python tool that makes sharing variables between SpaceBrew and python code as seemless as possible. 
* The opencvBackground is a openCV based background difference detector (motion sensor) that supports a region of interest (ROI) that can be remotely configured and viewed over SpaceBrew.
 
Documentation
  * In Progress 
 
************************************************
 SETUP 
************************************************
Hardware Requirements:
  * Machine capable of running python, node (spacebrew), and for the opencvBackground, OpenCV must be installed.
 
Dependencies:
  * python websocket-client library 
  	- 'pip install websocket-client'
    - Be aware that there is another python package called 'websocket' that uses the same package name. If you have websocket installed you will need to uninstall it before installing websocket-client. (You can uninstall if with 'pip uninstall websocket'.)
  * python feedparser 
    - 'pip install feedparser'
  * python opencv
    - Debian: sudo apt-get install python-opencv
    - OS X Macports: sudo port install opencv +python27 +universal
    - OS X Brew: brew install....  (I don't really know)
  * opencv dev files
    - Debian: sudo apt-get install libopencv-dev
    - OS X Macports: sudo port install opencv +python27 +universal
    - OS X Brew: ???

Local:
  1. Run a SpaceBrew server
  2. Open the SpaceBrew web admin
  3. Run the examples
 
 
************************************************
 MORE INFO 
************************************************
* To-Dos
  * 
 
* Troubleshooting
  *
 
* Credits
  * phooky (github) / Adam Mayer - For his work on the original spacebrew python api
 
* Licensing
  * Open-source (BSD license)
 
* Notes
  *