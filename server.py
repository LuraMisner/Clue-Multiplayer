import constants
import socket
import pickle
from _thread import *
from game import Game


# Running on local host
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((constants.SERVER, constants.PORT))
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


def add_to_all_logs(gameid, text):
    """
    Adds a message for all players in the game to see
    :param gameid: Integer, id of the game
    :param text: String, message for players
    """
    for character, p_log in log[gameid]:
        p_log.append(text)


def add_to_player_log(gameid, player,  text):
    """
    Adds a message for one player to see
    :param gameid: Integer, id of the game
    :param player: String representing the player
    :param text: String, message for the player
    """
    for character, p_log in log[gameid]:
        if character == player:
            p_log.append(text)


def get_player_log(gameid, player) -> [str]:
    """

    :param gameid:
    :param player:
    :return:
    """
    for character, p_log in log[gameid]:
        if character == player:
            if len(p_log) <= 6:
                return p_log
            else:
                return p_log[len(p_log) - 6:]


def threaded_client(connect, p, gameid):
    """
    Function that handles communication between the client and the server
    :param connect: Address of client
    :param p: Integer, player id
    :param gameid: Integer, game id
    """
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
                            log[gameid].append((character, []))
                        except Exception as err:
                            print("Error adding player: ", err)
                            reply = False

                    # Indicates the player is ready, check to see if all players in this game are ready
                    elif data == 'start':
                        ready[gameid][p] = True
                        reply = all(ready[gameid])
                        if reply and not game.get_split():
                            add_to_all_logs(gameid, 'Game started, cards distributed')
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
                            add_to_all_logs(gameid, f'{character} has been disqualified')

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

                        add_to_all_logs(gameid, f'{character} suggests {char}, {weapon}, {room}')

                    # Making an accusation
                    elif data[:15] == 'make_accusation':
                        char, weapon, room = data[16:].split(',')
                        game.make_accusation(character, char, weapon, room)

                        add_to_all_logs(gameid, f'{character} accuses {char}, {weapon}, {room}')

                    # Check if the last suggestion has been completed
                    elif data == 'check_suggestion_status':
                        reply = game.get_pending_suggestion()

                    # Client is submitting an answer to the question
                    elif data[:17] == 'answer_suggestion':
                        game.answer_suggestion(character, data[18:])

                        add_to_all_logs(gameid, f'{character} shows {game.get_suggestion_player()} a card')

                    # Check whose turn it is to answer a suggestion
                    elif data == 'waiting_on':
                        reply = game.get_waiting_on()

                    # Wait on the next player
                    elif data == 'next_player':
                        game.next_player()
                        add_to_all_logs(gameid, f'{character} has no cards to show')

                    # Get the response of a suggestion
                    elif data == 'get_suggestion_response':
                        reply = game.get_suggestion_response()

                        if character == game.get_suggestion_player():
                            # Add the response to the characters log
                            if reply != 'No one could disprove':
                                pl = game.get_suggestion_player_response()
                                add_to_player_log(gameid, character, f'{pl} shows you {reply}')
                            else:
                                add_to_player_log(gameid, character, reply)

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

                    # Get the envelope to display at the end
                    elif data == 'get_envelope':
                        reply = game.get_envelope()

                    # Gets data from the log (last 10 items)
                    elif data == 'get_log':
                        reply = get_player_log(gameid, character)

                    # Handles players closing the game early
                    elif data == 'early_quit':
                        game.early_quit(character)

                        add_to_all_logs(gameid, f'{character} has been disconnected. Cards distributed')

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
    """
    Accepts incoming connections, and places them into a game.
    Creates a new game if none are available.
    Starts the client on a thread
    """
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
