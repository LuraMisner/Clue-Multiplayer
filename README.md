# Clue-Multiplayer
Recreating the board game Clue in python

## Rules
This game follows the rules of the original board game, which can be found here:
https://www.cs.nmsu.edu/~kcrumpto/TAClasses/ClueRules.html#:~:text=In%20a%20Suggestion%2C%20the%20Room,and%20you%20are%20the%20winner.

The major changes are that the player does not have to leave a room and then re-enter it at a later turn to make another suggestion in the room, 
and that there is no suspect or weapon tokens that get transferred to the room when a suggestion is made.

## Controls
**Arrow keys** are used for movement of the player piece around the board.
**Mouse** presses are used for character selection, selecting an action to perform on the players turn, and for selecting items in suggestions and accusations.

## What you'll need
- Clone of the main repository 
- Python interpreter version 3.9 or greater https://www.python.org/downloads/
- Python environment (not required, but would make your life easier) *Suggestion: Pycharm, https://www.jetbrains.com/pycharm/download/#section=windows*
- Install the pygame library (add it to the project as a package in an environment, or perform "pip install pygame" via the console)

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
There are several ways to go about this, but I suggest trying out Hamachi *https://vpn.net/*.
Hamachi allows you to create a virtual server, allowing up to 5 people to join the server for free.
If you go this route, Hamachi will need to be installed on all participating devices, and one player will need to 
create a server. 

Once created, all participating members should join the server created.
This can be done by selecting Network > Join existing network ...

Continue through the set-up instructions, when it comes to the changing line 2 of constants.py, enter the servers 
IPv4 address in this location.
