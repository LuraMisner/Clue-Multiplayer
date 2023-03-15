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
s.listen(6)
print("Waiting for a connection, Server Started")

games = {}
ready = {}
log = {}
idCount = 0
gameId = 0


def threaded_client(connect, p, gameid):
    connect.send(str.encode(str(p)))
    character = None

    reply = ""
    while True:
        try:
            data = connect.recv(2048).decode()

            if gameId in games:
                game = games[gameid]

                if not data:
                    break
                else:
                    # Character selection
                    if data == 'character_selection':
                        reply = game.available_characters

                    # Make the player once the character has been selected
                    elif data in ['Colonel Mustard', 'Miss Scarlet', 'Mr.Peacock',
                                  'Mrs.White', 'Professor Plum', 'Reverend Green']:
                        # Make the player
                        try:
                            reply = game.add_player(data)
                            character = data
                        except Exception as err:
                            print("Error adding player: ", err)
                            reply = False

                    # Indicates the player is ready, check to see if all players in this game are ready
                    elif data == 'start':
                        ready[gameid][p] = True
                        reply = all(ready[gameid])
                        if reply and not game.get_split():
                            log[gameid].append('Game started, cards distributed')
                            game.split_cards()

                    # Tells client how many players are ready out of the players in this game
                    elif data == 'num_ready':
                        reply = [len(ready[gameid])]
                        num_ready = 0
                        for player in ready[gameid]:
                            if player:
                                num_ready += 1
                        reply.append(num_ready)

                    # Shows the client which cards they have been delt
                    elif data == 'get_cards':
                        reply = game.get_player_cards(character)

                        if not reply:
                            print(f"Error getting {character}'s cards")

                    # Shows the clients notes (differs from cards once they have learned information from other players)
                    elif data == 'get_notes':
                        reply = game.get_player_notes(character)

                    # Check whose turn it is
                    elif data == 'whos_turn':
                        reply = game.whos_turn()

                    # Check if a player is disqualified
                    elif data == 'check_disqualified':
                        reply = game.get_player_disqualification(character)
                        if reply:
                            log[gameid].append(f'{character} has been disqualified')

                    # Get the positions of all players
                    elif data == 'get_all_positions':
                        reply = game.get_all_player_locations()

                    # Player has finished their turn
                    elif data == 'turn_done':
                        game.increment_turn()

                    # Gets whose turn it is
                    elif data == 'turn':
                        reply = game.get_turn()

                    # Making a suggestion
                    elif data[:15] == 'make_suggestion':
                        char, weapon, room = data[16:].split(',')
                        game.make_suggestion(character, char, weapon, room)

                        log[gameid].append(f'{character} suggests {char}, {weapon}, {room}')

                    # Making an accusation
                    elif data[:15] == 'make_accusation':
                        char, weapon, room = data[16:].split(',')
                        game.make_accusation(character, char, weapon, room)

                        log[gameid].append(f'{character} accuses {char}, {weapon}, {room}')

                    # Check if the last suggestion has been completed
                    elif data == 'check_suggestion_status':
                        reply = game.get_pending_suggestion()

                    # Client is submitting an answer to the question
                    elif data[:17] == 'answer_suggestion':
                        game.answer_suggestion(data[18:])

                        log[gameid].append(f'{character} shows {game.get_suggestion_player()} a card')

                    # Check whose turn it is to answer a suggestion
                    elif data == 'waiting_on':
                        reply = game.get_waiting_on()

                    # Wait on the next player
                    elif data == 'next_player':
                        game.next_player()

                        log[gameid].append(f'{character} has no cards to show')

                    # Get the response of a suggestion
                    elif data == 'get_suggestion_response':
                        reply = game.get_suggestion_response()

                    # Get the last suggestion
                    elif data == 'get_last_suggestion':
                        reply = game.get_last_suggestion()

                    # Adds information to our notes section
                    elif data[:8] == 'add_note':
                        note = data[9:]
                        game.add_note(character, note)

                    # Updates a player position
                    elif data[:15] == 'update_position':
                        position = data[16:]
                        game.update_player_position(character, int(position))

                    # Check if the game has finished
                    elif data == 'game_finished':
                        reply = game.get_won()

                    # Gets the winner
                    elif data == 'get_winner':
                        reply = game.get_winner()

                    # Gets data from the log (last 10 items)
                    elif data == 'get_log':
                        if len(log[gameid]) <= 10:
                            reply = log[gameid]
                        else:
                            reply = log[gameid][len(log[gameid]) - 10:]

                    # Handles players closing the game early
                    elif data == 'early_quit':
                        game.early_quit(character)

                        log[gameid].append(f'{character} has been disconnected. Cards distributed')

                    connect.sendall(pickle.dumps(reply))
            else:
                break
        except Exception as er:
            print("Error: ", er)
            break

    if not games[gameid].get_won():
        # Remove the character if they disconnect early and distribute the cards between remaining players
        if character:
            games[gameid].early_quit(character)

    print("Lost connection")
    connect.close()


while True:
    # Accept any incoming connection
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1

    # If the game is full or already started, then move to a different game
    if gameId in games:
        if all(ready[gameId]) or len(ready[gameId]) == 6:
            gameId += 1

    # If the game does not exist, make a new one
    if gameId not in games:
        print("Creating a new game...")
        games[gameId] = Game(gameId)
        ready[gameId] = []
        log[gameId] = []
        idCount = 0

    ready[gameId].append(False)
    start_new_thread(threaded_client, (conn, idCount, gameId))
