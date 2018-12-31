NOTE: This game (called Carleton College: The Quest for Schiller) was my final project for Intro to Computer Science. It is programmed entirely by me in Python. I have included this as my portfolio to demonstrate my profeciency in Python. Some of the puzzles require specific knowledge about Carleton College, but there are hints that should allow you to get past this.
This document explains all of the different classes I used and how they function in the game.


Cayden Ehrlich
CS Final Project Winter 2017
Carleton College: The Quest for Schiller

My game is a text-based adventure game.

The first type of class is the Item class. This includes items that are moveable and not moveable. Non-moveable items are still able to be examined, which provides a much more interactive user experience. Each item has a list of IDs with which the user can refer to it. Each item ID is added to the game's items dictionary (itemsDict), where the ID is the key and the value is the item. This allows for translation between the user input and the actual methods. There are 3 subclasses of Item: Weapon, Armor, and Schillers. Weapons increase the user's maximum damage; Armor increases the user's defense against damage (the player can wear one helmet, one chest piece, one pair of leggings, and one pair of boots at the same time through the use of an armor slot system); Schillers are the game's currency.

Next is the Enemy class. The Enemy is able to attack the player. Attacks in this game are done using the random.gauss method from the random module. The mean is the attacker's maximum damage divided by 2.0, and the standard deviation is 1.5. When the enemy dies, it drops all of the items in its list of items to drop into the room it's in.

Next is the BasePuzzle class. This is a basic class that handles giving hints to the user and what to do when the puzzle is solved. The subclasses are SingleItemPuzzle, which is used for puzzles that just require one item to solve, and OrderPuzzle, which is used for puzzles where you have to do something in a certain order.

The BaseRoom class, like the Item class, has an ID and a rooms dictionary. It also has a dictionary that tells the computer the ID of the rooms in different directions in relation to the room. It also has a describe method which is called whenever the player moves into a room or inputs 'look'. It uses the given description of the room and also the location descriptions of the Items in the room (a location description being something like "There is a furnace in the corner"). There are three subclasses: EnemyRoom, a room that has an enemy in it (if the player tries to do something other than attack or get help in an EnemyRoom that still has an enemy, the function won't work and the enemy will attack the player); PuzzleRoom, a room that has a puzzle (this type of room can have a door that's locked until the player beats the puzzle); and Shop, a room where the player can buy equipment.

The last class is the Player. This is the class that the interpreter function (explained below) uses to call methods. This class also stores the user's inventory, HP, defense, damage, Schillers, etc.

The interpret function uses a dictionary of strings (made in the createCommandDicts function) with method values to translate user input into actual methods. There's one dictionary for commands that don't take arguments and a separate one for commands that do take arguments. It then uses the items dictionary to translate the item part of the user's input (if there is one). If the user inputs a string for a command that takes an argument and they don't put in an argument, the interpreter will ask for one.

The game function is where all of the actual items, enemies, puzzles, rooms, and player are defined. It's also where the asking for user input part of the game takes place. It also checks to make sure the player hasn't already died or won.

Everything in this program should work.

To run the program, just open it with the command prompt and play! I highly recommend typing in 'help' to get a list of functions.