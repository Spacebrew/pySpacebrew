import websocket
import thread
import time
import json


class SpaceBrew(object):
    # Define any runtime errors we'll need
    class ConfigurationError(Exception):
	def __init__(self, brew, explanation):
	    self.brew = brew
	    self.explanation = explanation
	def __str__(self):
	    return repr(self.explanation)

    class Slot(object):
	def __init__(self, name, brewType, default = None):
	    self.name = name
	    self.type = brewType
	    self.value = None
	    self.default = default
	def makeConfig(self):
	    d = { 'name':self.name, 'type':self.type, 'default':self.default }
	    return d
		
    class Publisher(Slot):
	pass

    class Subscriber(Slot):
	pass

    def __init__(self, name, description="", server="sandbox.spacebrew.cc", port=9000):
	self.server = server
	self.port = port
	self.name = name
	self.description = description
	self.connected = False
	self.publishers = []
	self.subscribers = []

    def addPublisher(self, name, brewType="string", default=None):
	if self.connected:
	    raise ConfigurationError(self,"Can not add a new publisher to a running SpaceBrew instance (yet).")
	else:
	    self.publishers.append(self.Publisher(name, brewType, default))
    
    def addSubscriber(self, name, brewType="string", default=None):
	if self.connected:
	    raise ConfigurationError(self,"Can not add a new subscriber to a running SpaceBrew instance (yet).")
	else:
	    self.subscribers.append(self.Subscriber(name, brewType, default))

    def makeConfig(self):
	subs = map(lambda x:x.makeConfig(),self.subscribers)
	pubs = map(lambda x:x.makeConfig(),self.publishers)
	d = {'config':{
		'name':self.name,
		'description':self.description,
		'publish':{'messages':pubs},
		'subscribe':{'messages':subs},
		}}
	return d


def sendMessage():
	message = { "message":
       {
           "clientName":"spacepython",
           "name":"coolBool",
           "type":"boolean",
           "value":"true"
       }
   	}
   	ws.send(json.dumps(message))

def on_message(ws, message):
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
    	myConfig = {"config":{
    	"name":"spacepython",
    	"description":"what what",
    	"publish":{"messages":[
    	{"name":"coolBool","type":"boolean","default":"1"},
    	{"name":"sendBool","type":"boolean","default":"boolean"}]},
    	"subscribe":{"messages":[{"name":"sbool","type":"boolean"}]}}}
    	print myConfig 
    	ws.send(json.dumps(myConfig))
    	
    	for i in range(60):
    		time.sleep(5)
    		sendMessage()
    thread.start_new_thread(run, ())




if __name__ == "__main__":
    brew = SpaceBrew("new brew")
    brew.addPublisher("pub")
    brew.addSubscriber("sub")
    print brew.makeConfig()
    print json.dumps(brew.makeConfig())
    myConfig = {"config":{
	    "name":"spacepython",
	    "description":"what what",
	    "publish":{"messages":[
		    {"name":"coolBool","type":"boolean","default":"1"},
		    {"name":"sendBool","type":"boolean","default":"boolean"}]},
	    "subscribe":{"messages":[{"name":"sbool","type":"boolean"}]}}}
    print myConfig 
    print json.dumps(myConfig)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:9000",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()
