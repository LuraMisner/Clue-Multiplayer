# Clue-Multiplayer
Recreating the board game Clue in python

## Rules
This game follows the rules of the original board game, which can be found here:
https://www.cs.nmsu.edu/~kcrumpto/TAClasses/ClueRules.html#:~:text=In%20a%20Suggestion%2C%20the%20Room,and%20you%20are%20the%20winner.

The major changes are that the player does not have to leave a room and then re-enter it at a later turn to make another suggestion in the room, 
and that there is no suspect or weapon tokens that get transferred to the room when a suggestion is made.

## Controls
Arrow keys are used for movement of the player piece around the board.
Mouse presses are used for character selection, selecting an action to perform on the players turn, and for selecting items in suggestions and accusations.

## Set-up
Works on multiple devices on the same network, or you may run it with multiple sessions on one device.
This repository will need to be cloned on all devices that are being used.
First, **one person must decide to be the host, they are the only person who needs to run server.py**

Before the host runs server.py, **everyone** will need to change **line 2 of constants.py** and replace the 'numbers.numbers.number.numbers' with a string of the **hosts IP**.
The host can find this by opening command prompt and typing "ipconfig" and entering the IPv4 address displayed, and relaying this information
to the participating parties.

After that, run the server file. If it is successful you will see "Waiting for a connection, Server Started" in the terminal.

Once the server is running, each player can run the client file to load the game.
The game will start when all players connected have selected and confirmed their character. 

### Want to play the game with friends online?
Try out Hamachi! The host will need to download and create a virtual server (for free), and put the servers IP address 
on line 2 of constants.py instead. Then continue through the set-up instructions as usual. 