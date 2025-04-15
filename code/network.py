import socket
import config

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = config.ip_server
        self.port = config.port
        self.addr = (self.server, self.port)
        self.role = None
        self.pos = None
        self.connect()
        
        

    def getPos(self): 
        return self.pos
    
    def getRole(self):
        return self.role
    
    def getstartrole(self):
        try:

            return self.client.recv(2048).decode
        
        except Exception as e:
            print("connection failed", e)

    def connect(self):
        try:
            data = self.client.connect(self.addr)

            self.role = self.client.recv(2048).decode()

            pos_str = self.client.recv(2048).decode()

            self.pos = tuple(map(int, pos_str.split(",")))
        
        except Exception as e:
            print("connection failed", e)
            


    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

            

