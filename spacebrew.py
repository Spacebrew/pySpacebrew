import websocket
import thread
import time
import json

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
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:9000",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()