import socket
from _thread import *
import sys


server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn))