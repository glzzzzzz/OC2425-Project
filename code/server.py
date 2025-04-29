# serveur.py
import socket, threading
from config import ip_server, port
import time 

pos   = [(600.0, 0.0), (100.0, 100.0)]
roles = ["chat", "souris"]
bomb_owner = 0
last_switch = time.time()

def read_msg(s):
    pos_str, owner = s.split("|")
    x_str, y_str = pos_str.split(",")
    return float(x_str), float(y_str), owner

def make_msg(t, owner):
    return f"{t[0]},{t[1]}|{owner}"

def handle_client(conn, player_id):
    global bomb_owner, pos, last_switch
    conn.sendall(roles[player_id].encode())
    conn.sendall(make_msg(pos[player_id], bomb_owner).encode())

    other = 1 - player_id
    try:
        while True:
            data = conn.recv(2048).decode()
            if not data: break

            x_f, y_f, owner = read_msg(data)
            pos[player_id] = (x_f, y_f)
            # Mise à jour du bomb_owner global
            if check_collision() :
                bomb_owner = 1 - bomb_owner
                last_switch = time.time()
            # On renvoie la position de l’autre + owner
            conn.sendall(make_msg(pos[other], roles[bomb_owner]).encode())
    finally:
        conn.close()

def check_collision() :
    if abs(pos[0][0]-pos[1][0])+abs(pos[0][1]-pos[1][1]) < 48 and time.time() - last_switch > 3.0:
        return True

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip_server, port))
    sock.listen()
    player_id = 0
    while True:
        conn, _ = sock.accept()
        threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()
        player_id = 1 - player_id

if __name__ == "__main__":
    main()
