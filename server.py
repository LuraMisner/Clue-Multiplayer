import socket
import pickle
from _thread import *
from game import Game


# Running on local host
server = "192.168.1.204"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

# Listen for connections ( Number indicates maximum amount of connections )
s.listen(2)
print("Waiting for a connection, Server Started")

games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == 'character_selection':
                        reply = game.available_characters
                    elif data in ['Colonel Mustard', 'Miss Scarlet', 'Mr.Peacock',
                                  'Mrs.White', 'Professor Plum', 'Reverend Green']:
                        # Make the player
                        try:
                            reply = game.add_player(data)
                        except Exception as e:
                            print("Error adding player: ", e)

                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except Exception as e:
            print("Error: ", e)
            break

    print("Lost connection")
    conn.close()


while True:
    # Accept any incoming connection
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    gameId = (idCount - 1) // 2

    # If the game does not exist, make a new one
    if gameId not in games:
        print("Creating a new game...")
        games[gameId] = Game(gameId)

    start_new_thread(threaded_client, (conn, idCount-1, gameId))
