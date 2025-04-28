# serveur.py
import socket
import threading
from config import ip_server, port

# positions initiales en float
pos   = [(600.0, 0.0), (100.0, 100.0)]
roles = ["chat", "souris"]

def read_pos(s):
    x_str, y_str = s.split(",")
    return float(x_str), float(y_str)

def make_pos(t):
    return f"{t[0]},{t[1]}"

def handle_client(conn, player_id):
    # Handshake
    conn.sendall(roles[player_id].encode())
    conn.sendall(make_pos(pos[player_id]).encode())

    other = 1 - player_id
    try:
        while True:
            data = conn.recv(2048).decode()
            if not data:
                break
            pos[player_id] = read_pos(data)
            conn.sendall(make_pos(pos[other]).encode())
    except Exception as e:
        print(f"[serveur] erreur thread {player_id} :", e)
    finally:
        conn.close()
        print(f"[serveur] connexion {player_id} fermée")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # permet de relancer rapidement après kill sans attendre le TIME_WAIT
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip_server, port))
    sock.listen()
    print(f"[serveur] écoute sur {ip_server}:{port}")

    player_id = 0
    while True:
        conn, addr = sock.accept()
        print(f"[serveur] Connexion #{player_id} reçue de {addr}")
        threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()
        # on alterne 0 ↔ 1
        player_id = 1 - player_id

if __name__ == "__main__":
    main()
