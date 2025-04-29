# network.py
import socket
from config import ip_server, port

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_server, port))

        # Handshake
        self.role = self.client.recv(2048).decode()
        pos_str = self.client.recv(2048).decode()  # "x,y|owner"
        ready,pos_part, owner_part = pos_str.split("|")
        x_f, y_f = map(float, pos_part.split(","))
        self.pos = (int(x_f), int(y_f))
        self.bomb_owner = owner_part
        self.ready = ready

    def getRole(self):
        return self.role

    def getPos(self):
        return self.pos

    def getBombOwner(self):
        return self.bomb_owner
    
    def getReady(self):
        return self.ready

    def sendRecieve(self, data: str):
        """
        data = "ready|x,y|owner"
        Returns "ready|x2,y2|owner"
        """
        try:
            self.client.sendall(data.encode())
            reply = self.client.recv(2048).decode()
            if not reply:
                return None
            ready, pos_part, owner_part = reply.split("|")
            x_f, y_f = map(float, pos_part.split(","))
            self.pos = (int(x_f), int(y_f))
            self.bomb_owner = owner_part
            self.ready = ready
            return f"{self.ready}|{self.pos[0]},{self.pos[1]}|{self.bomb_owner}"
        except socket.error as e:
            print("Socket error:", e)
            return None