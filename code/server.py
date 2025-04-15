import socket
from _thread import *
import sys
from config import ip_server, port


server = ip_server
port = port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")





def read_pos(str):
    str = str.split(",")
    return int(float(str[0])),int(float(str[1]))
    

def make_pos(tup):
    return str(int(tup[0])) + "," + str(int(tup[1]))



pos = [(600,0),(100,100)]

roles = ["chat", "souris"]
def threaded_client(conn, player):
    
    
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            reply = data
            pos[player] = data

            
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1 :
                    reply = pos[0]
                else: 
                    reply = pos[1]

                
            
            conn.sendall(str.encode(make_pos(reply)))

        except Exception as e:
            print("Error:", e)
    
    print("Lost connection")
    conn.close()

def threaded_client_role(conn, player):
    role = roles[player] if player < len(roles) else "spectateur"
    
    try:
        conn.sendall(role.encode())
        conn.sendall(str.encode(make_pos(pos[player])))
    except Exception as e :
        print("error", e)
        

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    start_new_thread(threaded_client_role,(conn, currentPlayer))
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    