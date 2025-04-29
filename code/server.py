# serveur.py
import socket, threading
from config import ip_server, port
import time 

class World() :
    def __init__(self):
        self.pos   = [(600.0, 0.0), (100.0, 100.0)]
        self.roles = ["chat", "souris"]
        self.bomb_owner = 0
        self.last_switch = time.time()
        self.ready = False

    def check_collision(self) :
        if abs(self.pos[0][0]-self.pos[1][0])+abs(self.pos[0][1]-self.pos[1][1]) < 48 and time.time() - self.last_switch > 3.0:
            return True
        
WORLD = World()

def read_msg(s):
    pos_str, owner = s.split("|")
    x_str, y_str = pos_str.split(",")
    return ready, float(x_str), float(y_str), owner

def make_msg(t, owner):
    return f"{ready}|{t[0]},{t[1]}|{owner}"

def handle_client(conn, player_id):
    conn.sendall(WORLD.roles[player_id].encode())
    conn.sendall(make_msg(WORLD.pos[player_id], WORLD.bomb_owner).encode())

    other = 1 - player_id
    try:
        while True:
            data = conn.recv(2048).decode()
            if not data: break

            WORLD.ready, x_f, y_f, owner = read_msg(data)
            WORLD.pos[player_id] = (x_f, y_f)
            # Mise à jour du bomb_owner global
            if WORLD.check_collision() :
                WORLD.bomb_owner = 1 - WORLD.bomb_owner
                WORLD.last_switch = time.time()
            # On renvoie la position de l’autre + owner
            conn.sendall(make_msg(WORLD.pos[other], WORLD.roles[WORLD.bomb_owner]).encode())
    finally:
        conn.close()


def main():
    global ready

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip_server, port))
    sock.listen()
    player_id = 0
    ready = False

    # Attente de la connexion du premier joueur
    conn1, _ = sock.accept()
    thread1 = threading.Thread(target=handle_client, args=(conn1, player_id))
    thread1.start()
    player_id = 1

    # Attente de la connexion du second joueur
    conn2, _ = sock.accept()
    thread2 = threading.Thread(target=handle_client, args=(conn2, player_id))
    thread2.start()
    ready = True

    # Attente que les deux threads clients se terminent
    thread1.join()
    thread2.join()

    sock.close()


if __name__ == "__main__":
    main()
