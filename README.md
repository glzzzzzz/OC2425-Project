# 💣 PASS THE BUCK

**PASS THE BUCK** est un jeu compétitif pour deux joueurs dans lequel le but est de se débarrasser d'une bombe avant qu'elle n'explose après 1 minute. Le tout dans une arène remplie de plateformes sur lesquelles vous pouvez rebondir !

---

## 🕹️ Description du jeu

- Jeu à 2 joueurs en réseau.
- Un joueur commence avec une **bombe** qui explosera après **1 minute**.
- Il faut toucher l'adversaire pour lui **passer la bombe**.
- Une fois la bombe transmise, le joueur qui s’en est débarrassé est **invulnérable pendant 3 secondes**.
- Contrôles :
  - **Joueur 1** : A (gauche), W (saut), D (droite)
  - **Joueur 2** : flèches gauche, haut, droite
- **Mécanique de rebond** : sautez contre les côtés des plateformes pour rebondir et gagner en mobilité.

---

## ⚙️ Installation du projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/pass-the-buck.git
cd pass-the-buck
```

### 2.  Créer un environnement virtuel et installer les dépendances

```bash
python -m venv env
source env/bin/activate      # macOS/Linux
env\Scripts\activate.bat     # Windows

pip install pygame-ce
pip install PyTMX
pip install setuptools
```

### 3. Ajouter le fichier de configuration
Dans le dossier ```/code```, crée un fichier ```config.py``` contenant :

```bash
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
TILE_SIZE = 32
ANIMATION_SPEED = 6
BOMB_TIMER = 60000  # Durée en millisecondes (1 minute)
ip_server = "votre_ip"
port = "le_port_de_votre_choix"
```
---
## 🧨 Lancer une partie

### 🖥️ Sur la première machine (serveur + joueur 1) :
1. Exécuter ```serveur.py``` pour lancer le serveur.
2. Exécuter ```main.py``` pour lancer la fenêtre du Joueur 1.

### 💻 Sur la deuxième machine (joueur 2) :
1. Exécuter ```main.py``` pour lancer la fenêtre du Joueur 2.

### ✅ Une fois les deux joueurs connectés, la partie commence automatiquement. Vous avez 60 secondes pour vous débarrasser de la bombe… Bonne chance !
---

## 🗂️ Structure du projet
```bash
OC2425-Projet/
├── code/
│   ├── config.py         # Fichier de configuration (à créer)
│   ├── level.py          # Création du niveau
│   ├── main.py           # Lancement du jeu
│   ├── network.py        # Communication client-serveur
│   ├── player.py         # Contrôle des joueurs
│   ├── serveur.py        # Script du serveur
│   ├── sprite.py         # Affichage des tuiles
│   └── timer.py          # Gestion du compte à rebours
│
├── data/
│   ├── fond_ciel.jpg         # Image de fond du ciel
│   ├── background/           # Éléments graphiques de la carte + test_map.tmx
│   │   └── test_map.tmx      # Carte du niveau
│   ├── angel/                # Skins du joueur 1
│   ├── monster/              # Skins du joueur 2
│   ├── bombe/                # Images de la bombe
│   └── Sons/                 # Musique et effets sonores
│
└── README.md                 # Ce fichier

```
