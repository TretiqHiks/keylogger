import socket
import threading
from datetime import date

HEADER = 64                                            #message length
PORT = 4567                                            #random unused port
#SERVER = socket.gethostbyname(socket.gethostname())   #server ip address
SERVER = "145.93.116.196"
ADDRESS = (SERVER, PORT)                               #socket address
FORMAT = "utf-8"                                       #encoding format
DISCONNECT_MSG = "!DSC"                                #disconnect message


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def printToFile(address, msg):
    f = open(f"logs\log[{address}][{date.today()}].txt", "a")
    f.write(msg)
    f.close()

def handle_client(conn, address):
    print(f"[CONNECTION] {address} connected.\n")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if(msg_length):
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if(msg == DISCONNECT_MSG):
                    connected = False
                    print(f"[{address}] Disconnected.")
                    break
                else:
                    printToFile(address, msg)
                print(f"[{address}] {msg}")
        except:
            connected = False
            print(f"[{address}] Disconnected.")
    conn.close()

def start():
    server.listen()
    while True:
        conn, address = server.accept()
        thread = threading.Thread(target=handle_client, args =(conn, address))
        thread.start()
        print(f"[Active connections] {threading.active_count() - 2}\n")



print(f"Server listening on {SERVER}")
start()
