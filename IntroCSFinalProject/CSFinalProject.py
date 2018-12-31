# Cayden Ehrlich
# Intro CS, Winter 2017
# Final Project: Carleton College - The Quest for Schiller

import random

def intro():
	# I got the ASCII Art for the title using a website (http://patorjk.com/software/taag/#p=display&f=Alpha&t=Type%20Something%20)
	print('''
		   ___           _      _                  ___      _ _                   
		  / __\__ _ _ __| | ___| |_ ___  _ __     / __\___ | | | ___  __ _  ___ _ 
		 / /  / _` | '__| |/ _ \ __/ _ \| '_ \   / /  / _ \| | |/ _ \/ _` |/ _ (_)
		/ /__| (_| | |  | |  __/ || (_) | | | | / /__| (_) | | |  __/ (_| |  __/_ 
		\____/\__,_|_|  |_|\___|\__\___/|_| |_| \____/\___/|_|_|\___|\__, |\___(_)
		                                                             |___/        

		  ________            ____                  __     ____              _____      __    _ ____         
		 /_  __/ /_  ___     / __ \__  _____  _____/ /_   / __/___  _____   / ___/_____/ /_  (_) / /__  _____
		  / / / __ \/ _ \   / / / / / / / _ \/ ___/ __/  / /_/ __ \/ ___/   \__ \/ ___/ __ \/ / / / _ \/ ___/
		 / / / / / /  __/  / /_/ / /_/ /  __(__  ) /_   / __/ /_/ / /      ___/ / /__/ / / / / / /  __/ /    
		/_/ /_/ /_/\___/   \___\_\__,_/\___/____/\__/  /_/  \____/_/      /____/\___/_/ /_/_/_/_/\___/_/     
		                                                                                                     

WELCOME TO CARLETON COLLEGE: THE QUEST FOR SCHILLER
For years now, the bust of Schiller, part of important Carleton College tradition, has been missing.
It's been so long since it's been seen that some students don't even think that the bust exists, and that it's just a \
joke made up by upperclassmen.
You know that the bust of Schiller is real, though. You may be the only one who still believes that it exists.
You've heard rumors that the bust has been stolen by monsters and is in a secret dungeon hidden under the first \
floor of the library. You, being a brave \
Carleton student, are determined to find the bust of Schiller and prove that it still exists, and so you have found the secret dungeon and are ready to find Schiller, \
whatever it takes.
Good luck.
Type help for a list of commands.
''')

# Item params = itemIDList, itemsDict, description, moveable, locDescript
class Item:
	'''This will be a base class for all items in the game - weapons, armor, gold, etc.'''
	def __init__(self, itemIDList, itemsDict, description, moveable, locDescript):
		'''
		itemIDList will be a list of the strings with which the player may refer to the item.
		itemsDict will be a dictionary in which all potential string references to an item will be stored as keys with the value being the actual item.
		description will be a string describing the item (ex: 'A shiny steel sword.').
		moveable will be a Boolean letting us know if the item can be moved. This will allow the player to still examine objects that can't be picked up.
		locDescript will be a description of where the item is (ex: 'There is a sword on the table.'). This will be changed if the item is dropped.
		'''
		self.descript = description
		self.moveable = moveable
		self.locDescript = locDescript
		self.itemIDList = itemIDList
		for itemID in self.itemIDList:
			itemsDict[itemID] = self
		self.itemType = 'item'
		if itemIDList[0][0] in ['a', 'e', 'i', 'o', 'u']:
			self.article = 'an'
		else:
			self.article = 'a'

	def getLocDescript(self):
		'''Describes where the item is.'''
		return self.locDescript

	def examine(self):
		'''Called by the Player class when the player wants a description of an item.'''
		return self.descript

# Weapon params = itemIDList, itemsDict, description, locDescript, damage
class Weapon(Item):
	def __init__(self, itemIDList, itemsDict, description, locDescript, damage):
		'''Weapons will increase the player's maximum possible damage.'''
		self.moveable = True
		Item.__init__(self, itemIDList, itemsDict, description, self.moveable, locDescript)
		self.damage = damage
		self.equipped = False
		self.itemType = 'weapon'

	def examine(self):
		'''Weapons have their own examine function so that it will also show the damage and whether or not it is equipped.'''
		weaponDescript = self.descript
		weaponDescript += ' ({} damage)'.format(self.damage)
		if self.equipped:
			weaponDescript += '   (Equipped)'		
		return weaponDescript

# Armor params = itemIDList, itemsDict, description, locDescript, defense, armorSlot
class Armor(Item):
	def __init__(self, itemIDList, itemsDict, description, locDescript, defense, armorSlot):
		'''Armor will increase the player's defense against enemies. The player will be able to have one helmet, one chest piece, one pair of leggings, and one pair of boots.'''
		self.moveable = True
		Item.__init__(self, itemIDList, itemsDict, description, self.moveable, locDescript)
		self.defense = defense
		self.isEquipped = False
		self.armorSlot = armorSlot
		self.itemType = 'armor'

	def examine(self):
		'''Similar to the weapon examine function, but defense instead of damage. Also says which slot the armor can fill.'''
		armorDescript = self.descript
		armorDescript += ' ({} defense. {})'.format(self.defense, self.armorSlot) 
		if self.equipped:
			armorDescript += '   (Equipped)'
		return armorDescript

# Schillers params = itemsDict, locDescript, value
class Schillers(Item):
	def __init__(self, itemsDict, locDescript, value):
		moveable = True
		self.value = value
		descript = "A coin with Schiller's bust on one side. The other side has the number {} on it.".format(self.value)
		Item.__init__(self, ['schillers', 'coins', 'gold', '{} schillers'.format(self.value)], itemsDict, descript, moveable, locDescript)
		self.itemType = 'schillers'
		self.article = str(self.value)

# Enemy params = enemyID, enemiesList, HP, damage, defense, itemsToDrop
class Enemy:
	# Note: itemsToDrop will be a list of actual items, not just strings; must initiate items BEFORE enemies
	def __init__(self, enemyID, enemiesList, HP, maxDamage, defense, itemsToDrop):
		self.enemyID = enemyID
		self.HP = HP
		self.maxDamage = maxDamage
		self.defense = defense
		self.itemsToDrop = itemsToDrop
		self.enemiesList = enemiesList
		self.enemiesList.append(self)

	def isAlive(self):
		if self.HP > 0:
			return True
		else:
			return False

	def attackPlayer(self, Player):
		damage = int(random.gauss(self.maxDamage/2.0, 1.5))
		damMinusDef = damage - Player.defense
		if damMinusDef < 0:
			damMinusDef = 0
		Player.HP -= damMinusDef
		if damMinusDef > 0:
			msg = '{} attacks you for {} damage! You have {} HP left.'.format(self.enemyID.capitalize(), damMinusDef, Player.HP)
			if damage > self.maxDamage:
				msg = 'CRITICAL HIT! ' + msg
		else:
			msg = '{} missed! You have {} HP left.'.format(self.enemyID.capitalize(), Player.HP)
		return msg

	def die(self, room):
		room.hasEnemy = False
		self.enemiesList.remove(self)
		dropsNameList = []
		for item in self.itemsToDrop:
			room.dropIntoRoom(item)
			dropsNameList.append(item.article + ' ' + item.itemIDList[0])
		if len(dropsNameList) > 1:
			dropsNameStr = ', '.join(dropsNameList[:-1])
			dropsNameStr += ' and {}'.format(dropsNameList[-1])
		else:
			dropsNameStr = ''.join(dropsNameList)
		return '{} died, dropping {}.'.format(self.enemyID.capitalize(), dropsNameStr)

class BasePuzzle:
	def __init__(self, puzzleDescription, victoryMsg, hintsList, puzzlesList):
		self.hintsList = hintsList
		self.victoryMsg = victoryMsg
		self.hintsCounter = 1
		self.solved = False
		self.puzzleDescription = puzzleDescription
		self.puzzlesList = puzzlesList
		self.puzzlesList.append(self)

	def solve(self):
		self.solved = True
		self.puzzlesList.remove(self)
		self.puzzleDescription = 'This puzzle has been solved.'
		return self.victoryMsg

	def getHints(self):
		'''This will give the user hints from the list of hints if they need it. They will get one more hint (if there are more) each time they ask.'''
		givenHintsList = []
		for hintIndex in range(self.hintsCounter):
			givenHintsList.append(self.hintsList[hintIndex])
		if self.hintsCounter < len(self.hintsList):
			self.hintsCounter += 1
		hintsStr = '\n'.join(givenHintsList)
		return hintsStr

# SingleItemPuzzle params = puzzleDescription, victoryMsg, hintsList, puzzlesList, itemToUse
class SingleItemPuzzle(BasePuzzle):
	def __init__(self, puzzleDescription, victoryMsg, hintsList, puzzlesList, itemToUse):
		BasePuzzle.__init__(self, puzzleDescription, victoryMsg, hintsList, puzzlesList)
		self.itemToUse = itemToUse
		self.puzType = 'single'

	def solveAttempt(self, itemObj, Player):
		if itemObj == self.itemToUse:
			Player.inventory.remove(itemObj)
			return BasePuzzle.solve(self)
		else:
			return 'Nothing happens.'

# OrderPuzzle params = puzzleDescription, victoryMsg, hintsList, puzzlesList, objectOrderList, newLocDescript
class OrderPuzzle(BasePuzzle):
	def __init__(self, puzzleDescription, victoryMsg, hintsList, puzzlesList, objectOrderList, newLocDescript):
		BasePuzzle.__init__(self, puzzleDescription, victoryMsg, hintsList, puzzlesList)
		self.objectOrderList = objectOrderList
		self.playerObjectUse = []
		self.puzType = 'order'
		self.newLocDescript = newLocDescript

	def solveAttempt(self, itemObj, Player):
		self.playerObjectUse.append(itemObj)
		if self.newLocDescript != '':
			itemObj.locDescript = 'The {} {}'.format(itemObj.itemIDList[0], self.newLocDescript)
		latestIndex = len(self.playerObjectUse) - 1
		if self.playerObjectUse[latestIndex] == self.objectOrderList[latestIndex]:
			if len(self.playerObjectUse) == len(self.objectOrderList):
				return BasePuzzle.solve(self)
			else:
				return "You hear something happening...maybe gears turning? It seems like you made the right choice."
		else:
			self.playerObjectUse = []
			return "Nothing happens...you must have made a wrong choice. Try again."

# BaseRoom params = roomID, roomsDict, directionsDict, description, itemsList
class BaseRoom:
	def __init__(self, roomID, roomsDict, directionsDict, description, itemsList):
		self.directionsDict = directionsDict
		self.descript = description
		self.itemsList = itemsList
		self.roomID = roomID
		roomsDict[self.roomID] = self
		self.roomsDict = roomsDict
		self.hasEnemy = False
		self.hasPuzzle = False
		self.isShop = False

	def isLegalMove(self, direct):
		shortDirect = direct[0]
		return shortDirect in self.directionsDict

	def getMoveDestination(self, direct):
		newRoomStr = self.directionsDict[direct]
		newRoom = self.roomsDict[newRoomStr]
		return newRoom

	def canTake(self, item):
		if item in self.itemsList:
			return True
		else:
			return False

	def takeFromRoom(self, item):
		self.itemsList.remove(item)

	def dropIntoRoom(self, item):
		item.locDescript = 'There is/are {} {} on the floor.'.format(item.article, item.itemIDList[0])
		self.itemsList.append(item)

	def describe(self):
		totalDescriptionL = []
		totalDescriptionL.append(self.descript)	
		for item in self.itemsList:
			if item.getLocDescript() != '':
				totalDescriptionL.append('\n' + item.getLocDescript())
		descriptionStr = ' '.join(totalDescriptionL)
		totalDescription = (self.roomID.upper() + '\n') + descriptionStr
		return totalDescription

# EnemyRoom params = roomID, roomsDict, directionsDict, description, itemsList, enemy
class EnemyRoom(BaseRoom):
	def __init__(self, roomID, roomsDict, directionsDict, description, itemsList, enemyObj):
		BaseRoom.__init__(self, roomID, roomsDict, directionsDict, description, itemsList)
		self.hasEnemy = True
		self.enemy = enemyObj

	def describe(self):
		description = BaseRoom.describe(self)
		if self.hasEnemy:
			description += '\nThere is a(n) {} in the room!'.format(self.enemy.enemyID)
		return description

# PuzzleRoom params = roomID, roomsDict, directionsDict, description, itemsList, puzzle, lockedDirectionDict, puzzPrizes
class PuzzleRoom(BaseRoom):
	def __init__(self, roomID, roomsDict, directionsDict, description, itemsList, puzzle, lockedDirectionDict, puzzPrizes):
		BaseRoom.__init__(self, roomID, roomsDict, directionsDict, description, itemsList)
		self.hasPuzzle = True
		self.puzzle = puzzle
		self.lockedDirectionDict = lockedDirectionDict
		self.puzzPrizes = puzzPrizes

	def describe(self):
		noPuzDescript = BaseRoom.describe(self)
		PuzDescript = noPuzDescript + '\n{}'.format(self.puzzle.puzzleDescription)
		if self.lockedDirectionDict != {}:
			directionTranslator = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West'}
			directionKey = ''.join(self.lockedDirectionDict.keys())
			self.fullDirection = directionTranslator[directionKey]
			PuzDescript += '\nThere is a locked door to the {}.'.format(self.fullDirection)
		return PuzDescript

	def puzzleSolve(self, itemObj, Player):
		msg = self.puzzle.solveAttempt(itemObj, Player)
		if self.puzzle.solved:
			self.hasPuzzle = False
			prizesNameList = []
			for item in self.puzzPrizes:
				BaseRoom.dropIntoRoom(self, item)
				prizesNameList.append(item.itemIDList[0])
			if len(prizesNameList) > 1:
				prizesNameStr = ', a '.join(prizesNameList[:-1])
				prizesNameStr += ', and a {}'.format(prizesNameList[-1])
			else:
				prizesNameStr = ''.join(prizesNameList)
			msg += '\nA {} appear in the room as a prize for solving the puzzle.'.format(prizesNameStr)
			self.directionsDict.update(self.lockedDirectionDict)
			self.lockedDirectionDict = {}
			self.descript += '\nThere is an unlocked door to the {}.'.format(self.fullDirection)
			return msg
		else:
			return msg

# Shop params = roomsDict, directionsDict, description, shopDict
class Shop(BaseRoom):
	def __init__(self, roomsDict, directionsDict, description, shopDict):
		self.directionsDict = directionsDict
		self.descript = description
		self.shopDict = shopDict
		self.roomID = 'shop'
		roomsDict[self.roomID] = self
		self.itemsList = []
		for key in self.shopDict:
			self.itemsList.append(key)
		self.roomsDict = roomsDict
		self.hasEnemy = False
		self.hasPuzzle = False
		self.isShop = True

	def hasItem(self, itemObj):
		return itemObj in self.shopDict

	def getPrice(self, itemObj):
		return self.shopDict[itemObj]

	def dropIntoRoom(self, item):
		return "You can't drop that here!"

	def takeFromRoom(self, item):
		return "That would be stealing, and a good Carl would never steal."

	def listWares(self):
		waresList = []
		for item in self.shopDict:
			str = '{}: {} schillers'.format(item.itemIDList[0], self.shopDict[item])
			waresList.append(str)
		waresStr = '\n'.join(waresList)
		return waresStr

	def describe(self):
		if self.shopDict != {}:
			waresStr = '-------\nSHOP WARES:\n-------\n'
			waresStr += self.listWares()
		else:
			waresStr = "You've bought everything!"
		return self.descript + '\n' + waresStr

	def buyFromShop(self, itemObj):
		del self.shopDict[itemObj]

# Player params = currentRoom
class Player:
	def __init__(self, startRoom):
		self.currentRoom = startRoom
		self.inventory = []
		self.HP = 100
		self.maxDamage = 6
		self.defense = 0
		# This will allow there to be multiple types of armor.
		self.armor = {'helmet': None, 'chest': None, 'legs': None, 'boots': None}
		self.weapon = None
		self.schillers = 0

	def isAlive(self):
		if self.HP > 0:
			return True
		else:
			return False

	def equipArmor(self, armor):
		armor.equipped = True
		if self.armor[armor.armorSlot] != None:
			self.armor[armor.armorSlot].equipped = False
			self.defense += armor.defense - self.armor[armor.armorSlot].defense
		else:
			self.defense += armor.defense
		self.armor[armor.armorSlot] = armor
		return 'Equipped.'

	def equipWeapon(self, weapon):
		self.maxDamage = 5 + weapon.damage
		weapon.equipped = True
		if self.weapon != None:
			self.weapon.equipped = False
		self.weapon = weapon
		return 'Equipped.'

	# METHODS THAT WILL BE CALLED BY INTERPRETER
	def getHP(self):
		return self.HP

	def move(self, direction):
		if self.currentRoom.isLegalMove(direction):
			newRoom = self.currentRoom.getMoveDestination(direction)
			self.currentRoom = newRoom
			return self.currentRoom.describe()
		else:
			return 'You can\'t go there!'

	def displayInventory(self):
		inventoryDesc = ['----', 'health: {}'.format(self.HP), 'damage: {}'.format(self.maxDamage), 'defense: {}'.format(self.defense), '----', '']
		for item in self.inventory:
			inventoryDesc.append(item.examine())
		inventoryDesc = '\n'.join(inventoryDesc)
		inventoryDesc += '\n{} SCHILLERS'.format(self.schillers)
		return inventoryDesc

	def take(self, item):
		if self.currentRoom.isShop:
			return "That would be stealing, and a good Carl would never steal."
		elif self.currentRoom.canTake(item) and item.moveable:
			if item.itemType == 'schillers':
				self.schillers += item.value
			else:
				self.inventory.append(item)
			self.currentRoom.takeFromRoom(item)
			if item.itemType == 'weapon' or item.itemType == 'armor':
				response = input('Would you like to equip {}? (Y/N) '.format(item.itemIDList[0]))
				while response[0].lower() != 'y' and response[0].lower() != 'n':
					response = input('Please enter a valid string. Would you like to equip {}? (Y/N) '.format(item.itemIDList[0]))
				if response[0].lower() == 'y':
					return self.equip(item)
			return 'Taken.'

		elif item in self.inventory:
			return 'You already have that item.'

		elif not item.moveable:
			return "You can't take that."

		else:
			return 'That item is not in this room.'

	def drop(self, item):
		if self.currentRoom.isShop:
			return "You can't drop that here!"
		if item in self.inventory:
			self.inventory.remove(item)
			self.currentRoom.dropIntoRoom(item)
			return 'Dropped.'
		else:
			return "You can't drop that item, it isn't in your inventory."

	def look(self):
		return self.currentRoom.describe()

	def equip(self, item):
		if item in self.inventory:
			if item.itemType == 'armor':
				return self.equipArmor(item)
			elif item.itemType == 'weapon':
				return self.equipWeapon(item)
			else:
				return 'This item cannot be equipped.'
		else:
			return 'You don\'t have one of those.'

	def attack(self):
		if self.currentRoom.hasEnemy:
			enemy = self.currentRoom.enemy
			msg = ''
			if enemy.isAlive() and self.isAlive():
				damage = int(random.gauss(self.maxDamage/2.0, 1.5))
				damMinusDef = damage - enemy.defense
				if damMinusDef < 0:
					damMinusDef = 0
				enemy.HP -= damMinusDef
				if damMinusDef > 0:
					if damage > self.maxDamage:
						msg += 'CRITICAL HIT! '
					msg += 'You attack {} for {} damage! {} has {} HP left.\n'.format(enemy.enemyID, damMinusDef, enemy.enemyID.capitalize(), enemy.HP)
				else:
					msg += 'You missed! {} has {} HP left.\n'.format(enemy.enemyID.capitalize(), enemy.HP)
			if enemy.isAlive() and self.isAlive():
				# Check again to see if both are alive
				msg += enemy.attackPlayer(self)
			if not self.isAlive():
				msg += '\nYOU HAVE DIED.'
			if not enemy.isAlive():
				msg += '\n' + enemy.die(self.currentRoom)
			return msg
		else:
			return 'There is nothing for you to attack in this room.'

	def examineItem(self, item):
		return item.examine()

	def useItem(self, itemObj):
		if self.currentRoom.hasPuzzle and (itemObj in self.currentRoom.itemsList or itemObj in self.inventory):
			if itemObj in self.inventory:
				noReturnMsg = self.currentRoom.dropIntoRoom(itemObj)
				if self.currentRoom.puzzle.puzType == 'order':
					itemObj.locDescript = self.currentRoom.puzzle.newLocDescript
				else:
					itemObj.locDescript = ''
			return self.currentRoom.puzzleSolve(itemObj, self)
		else:
			return "You can't use that here."

	def getHints(self):
		if self.currentRoom.hasPuzzle:
			return self.currentRoom.puzzle.getHints()
		else:
			return "There are no hints for this room."

	def buy(self, itemObj):
		if self.currentRoom.isShop:
			if self.currentRoom.hasItem(itemObj):
				price = self.currentRoom.getPrice(itemObj)
				if price > self.schillers:
					return "You don't have enough schillers."
				else:
					self.schillers -= price
					self.currentRoom.buyFromShop(itemObj)
					self.inventory.append(itemObj)
					if itemObj.itemType == 'weapon' or itemObj.itemType == 'armor':
						response = input('Would you like to equip {}? (Y/N) '.format(itemObj.itemIDList[0]))
						while response[0].lower() != 'y' and response[0].lower() != 'n':
							response = input('Please enter a valid string. Would you like to equip {}? (Y/N) '.format(itemObj.itemIDList[0]))
						if response[0].lower() == 'y':
							return self.equip(itemObj)

			else:
				return "The shop doesn't have that."
		else:
			return "You are not in a shop."

def helpString():
	helpMsg = '''
	----------------------------------------------
	| CARLETON COLLEGE: THE QUEST FOR SCHILLER   |
	| Written and programmed by Cayden Ehrlich   |
	| CS 111, Winter 2017                        |
	----------------------------------------------
Carleton College: The Quest For Schiller is a text-based adventure game. NOTE: although only some possible inputs are shown here, there are \
other logical inputs that will also work for these same commands (for example, instead of 'take <item>', \
you can also say 'grab <item>' or 'pick up <item>' to do the same thing.).

**COMMANDS**
'take <item>' or 't <item>': takes item from current room
'drop <item>' or 'd <item>': drops item into current room
'examine <item>' or 'x <item>': gives a description of the item
'equip <item>' or 'q <item>': equips a weapon or armor
'use <item>' or 'u <item>': uses an item
'buy <item>' or 'b <item>': buys an item from the shop (must be in the shop to use)

'look' or 'l': describes the current room
'attack' or 'a': attacks the monster in the current room (if there is one)
'health': displays how much health you have left
'inventory' or 'i': displays your inventory
'exit' or 'quit': closes game

'north' or 'n': moves north (if possible)
'south' or 's': moves south (if possible)
'east' or 'e': moves east (if possible)
'west' or 'w': moves west (if possible)

HINTS: Almost every object in the game is examinable, even if you can't pick it up! Try examining items; they may help you with puzzles!
'''
	return helpMsg

def createCommandDicts(Player):
	comWithArgsDict = {
		'take': Player.take, 'get': Player.take, 'grab': Player.take, 't': Player.take, 'pick up': Player.take,
		'drop': Player.drop, 'leave': Player.drop, 'd': Player.drop, 'put down': Player.take,
		'examine': Player.examineItem, 'x': Player.examineItem, 'look at': Player.examineItem,
		'equip': Player.equip, 'q': Player.equip,
		'use': Player.useItem, 'u': Player.useItem, 'throw': Player.useItem,
		'buy': Player.buy, 'b': Player.buy	 
	}

	comNoArgsDict = {
		'look': Player.look, 'describe': Player.look, 'l': Player.look,
		'attack': Player.attack, 'a': Player.attack,
		'health': Player.getHP, 'hp': Player.getHP,
		'inventory': Player.displayInventory, 'equipment': Player.displayInventory, 'i': Player.displayInventory,
		'help': helpString, 'h': helpString,
		'hint': Player.getHints, 'hints': Player.getHints
	}

	return comWithArgsDict, comNoArgsDict

def interpret(Player, itemsDict, playerCommand):
	'''NOTE: all of these return rather than print. This is because the function that actually runs the game will print the output of this function.'''
	comWithArgsDict, comNoArgsDict = createCommandDicts(Player)

	playerCommand = playerCommand.lower()
	splitCommand = playerCommand.split()
	directionsList = ['north', 'n', 'south', 's', 'east', 'e', 'west', 'w']
	twoWordComm = ' '.join(splitCommand[0:2])

	if Player.currentRoom.hasEnemy and not (playerCommand == 'attack' or playerCommand == 'a' or playerCommand == 'help'):
		'''If the player's current room has an enemy and the player tries to do something other than attack, they will get this
		message and the enemy will attack them.'''
		errorMsg = "You are in battle with an enemy! You can't do that!\n"
		errorMsg += Player.currentRoom.enemy.attackPlayer(Player)
		return errorMsg

	elif playerCommand in directionsList:
		'''If the command is a direction, the player will move in that direction.'''
		direction = playerCommand[0]
		return Player.move(direction)

	elif len(splitCommand) == 1:
		'''If the input is only one word and isn't direction, this will attempt to translate it using the dictionary of commands without arguments.
		If the input is a command that takes an argument, the program will ask for that argument.'''
		if playerCommand in comNoArgsDict:
			actualCommand = comNoArgsDict[splitCommand[0]]
			return actualCommand()
		elif playerCommand in comWithArgsDict:
			argStr = input('What would you like to ' + playerCommand + '? ')
			playerCommand += ' ' + argStr
			return interpret(Player, itemsDict, playerCommand)
		else:
			return "I don't understand."

	elif splitCommand[0] in comWithArgsDict:
		commandStr = splitCommand.pop(0)
		argStr = ' '.join(splitCommand)
		if argStr in ['schillers', 'gold', 'coins']:
			for item in Player.currentRoom.itemsList:
				if item.itemIDList[0] == 'schillers':
					arg = item
		else:
			if argStr in itemsDict:
				arg = itemsDict[argStr]
			else:
				return "I don't recognize that object."
		actualCommand = comWithArgsDict[commandStr]
		return actualCommand(arg)

	elif twoWordComm in comWithArgsDict:
		commandLst = [splitCommand.pop(0)]
		commandLst.append(splitCommand.pop(0))
		commandStr = ' '.join(commandLst)
		argStr = ' '.join(splitCommand)
		if argStr in ['schillers', 'gold', 'coins']:
			for item in Player.currentRoom.itemsList:
				if item.itemIDList[0] == 'schillers':
					arg = item
			else:
				if argStr in itemsDict:
					arg = itemsDict[argStr]
				else:
					return "I don't recognize that object."
		actualCommand = comWithArgsDict[commandStr]
		return actualCommand(arg)

	else:
		return "I don't recognize that command."

	'''elif splitCommand[-1] in itemsDict:
		argStr = splitCommand.pop()
		arg = itemsDict[argStr]
		commandStr = ' '.join(splitCommand)
		if commandStr in comWithArgsDict:
			actualCommand = comWithArgsDict[commandStr]
			return actualCommand(arg)
		else:
			return "I don't recognize that command."

	elif len(splitCommand) > 2 and twoWordNoun in itemsDict:
		argStr = twoWordNoun
		arg = itemsDict[argStr]
		commandStr = ' '.join(splitCommand[0:-2])
		if commandStr in comWithArgsDict:
			actualCommand = comWithArgsDict[commandStr]
			return actualCommand(arg)
		else:
			return "I don't recognize that command." '''


'''MAKE SURE TO INCLUDE DOORS IN ROOM DESCRIPTIONS'''

	# Item params = itemIDList, itemsDict, description, moveable, locDescript
	# Armor params = itemIDList, itemsDict, description, locDescript, defense, armorSlot
	# Weapon params = itemIDList, itemsDict, description, locDescript, damage
def game():
	itemsDict = {}
	roomsDict = {}
	enemiesList = []
	puzzlesList = []

	'''***ITEMS***'''
	# Schiller Room
	SchillerBust = Item(['schiller', 'bust', 'schiller bust'], itemsDict, 'The prized bust of Friedrich von Schiller.', True, 'The bust of Schiller sits on a pedestal in the middle of the room.')
	pedestal = Item(['pedestal'], itemsDict, 'A simple marble pedestal. It has an enscription, but you can\'t read it.', False, '')

	# BOSS ROOM
	schillers15 = Schillers(itemsDict, '', 15)

	# Laundry Room
	LaundryMaschine = Item(['laundry machine', 'machine', 'washing machine'], itemsDict, 'A basic laundry machine.', False, 'There\'s a small laundry machine in the middle of the room...')
	SPSword = Weapon(['Sword of Stevie P', 'sword of stevie p', 'sword of stevie p', 'sword', 'swordofsteviep'], itemsDict, 
						'A glowing blade with "Steven Poskanzer" carved into the blade in calligraphy.', '', 15)

	# Levers Room
	lever1 = Item(['lever 1', '1', 'lever1'], itemsDict, 'A lever with the number "1" carved into the stone above it.', False, '')
	lever2 = Item(['lever 2', '2', 'lever2'], itemsDict, 'A lever with the number "2" carved into the stone above it.', False, '')
	lever3 = Item(['lever 3', '3', 'lever3'], itemsDict, 'A lever with the number "3" carved into the stone above it.', False, '')
	lever4 = Item(['lever 4', '4', 'lever4'], itemsDict, 'A lever with the number "4" carved into the stone above it.', False, '')
	lever5 = Item(['lever 5', '5', 'lever5'], itemsDict, 'A lever with the number "5" carved into the stone above it.', False, '')
	lever6 = Item(['lever 6', '6', 'lever6'], itemsDict, 'A lever with the number "6" carved into the stone above it.', False, '')
	lever7 = Item(['lever 7', '7', 'lever7'], itemsDict, 'A lever with the number "7" carved into the stone above it.', False, '')
	lever8 = Item(['lever 8', '8', 'lever8'], itemsDict, 'A lever with the number "8" carved into the stone above it.', False, '')
	lever9 = Item(['lever 9', '9', 'lever9'], itemsDict, 'A lever with the number "9" carved into the stone above it.', False, '')
	lever0 = Item(['lever 0', '0', 'lever0'], itemsDict, 'A lever with the number "0" carved into the stone above it.', False, '')

	frisbee = Item(['frisbee', 'disc', 'disk'], itemsDict, 'A Carleton College frisbee like the ones given to freshmen, but the year has been rubbed out.', True, 'There is a frisbee on the floor.')

	# Color Room
	table = Item(['table'], itemsDict, 'A simple wooden table.', False, 'There is a table in the center of the room.')
	maizeDisk = Item(['maize disk', 'gold disk', 'maize', 'maizedisk'], itemsDict, 'A maize disk.', True, 'There is a maize disk on the table.')
	greenDisk = Item(['green disk', 'green', 'greendisk'], itemsDict, 'A green disk.', True, 'There is a green disk on the table.')
	redDisk = Item(['red disk', 'red', 'reddisk'], itemsDict, 'A red disk.', True, 'There is a red disk on the table.')
	blueDisk = Item(['blue disk', 'blue', 'bluedisk'], itemsDict, 'A blue disk.', True, 'There is a blue disk on the table.')
	purpleDisk = Item(['purple disk', 'purple', 'purpledisk'], itemsDict, 'A purple disk.', True, 'There is a purple disk on the table.')

	schillers6 = Schillers(itemsDict, '', 6)

	# Workout Room
	KnightHelm = Armor(['knight helmet', 'knight helm', 'helmet', 'helm', 'knighthelmet', 'knighthelm'], itemsDict, 'A beautiful golden helmet with blue plumes; it resembles the knight on the \
		Carleton College logo', '', 8, 'helmet')

	# Furnace Room
	schillers10 = Schillers(itemsDict, '', 10)
	furnace = Item(['furnace'], itemsDict, 'It doesn\'t look like this furnace has had a fire in it for decades...it wouldn\'t be safe to use.', False, 'There\'s an old furnace in the corner.')

	# Shop
	# Armor params = itemIDList, itemsDict, description, locDescript, defense, armorSlot
	leatherCap = Armor(['leather cap', 'cap'], itemsDict, 'A simple leather cap.', '', 1, 'helmet')
	leatherTunic = Armor(['leather tunic', 'tunic'], itemsDict, 'A simple leather tunic.', '', 3, 'chest')
	leatherLeggings = Armor(['leather leggings', 'leggings'], itemsDict, 'Simple leather leggings.', '', 2, 'legs')
	leatherBoots = Armor(['leather boots', 'boots'], itemsDict, 'Simple leather boots.', '', 1, 'boots')

	# Prison
	dagger = Weapon(['dagger', 'dag'], itemsDict, 'A small, simple dagger.', '', 4)
	schillers8 = Schillers(itemsDict, '', 8)
	art = Item(['art'], itemsDict, 'A series of paintings that follow the life of Schiller from his birth to his death. They each say the year that the painting represents: the first one, of his \
birth, says 1759; the last, of his death, says 1805.', False, 'There\'s some art illustrating Schiller\'s life along the walls.')

	'''***ENEMIES***'''
	# Enemy params = enemyID, enemiesList, HP, damage, defense, itemsToDrop
	goblin = Enemy('small goblin', enemiesList, 8, 3, 0, [dagger, schillers8])
	skeleton = Enemy('spooky scary skeleton', enemiesList, 15, 4, 0, [schillers10])
	orc = Enemy('big smelly orc', enemiesList, 20, 10, 3, [SPSword])
	dragon = Enemy('giant dragon', enemiesList, 80, 25, 4, [schillers15])

	'''***PUZZLES***'''
	# SingleItemPuzzle params = puzzleDescription, victoryMsg, hintsList, puzzlesList, itemToUse
	# OrderPuzzle params = puzzleDescription, victoryMsg, hintsList, puzzlesList, objectOrderList, newLocDescript
	LeversPuzzle = OrderPuzzle('There are 10 levers lined up along the Eastern wall; they are numbered 0-9. There is an inscription above the levers - "Only true lovers of Schiller may find \
him, thus you must answer this question: In what year was Friedrich von Schiller born?"', 'You hear whirring behind the Eastern wall; it seems like you got the answer right!',
		['1. If only you knew more about Schiller\'s life...is there anything in this dungeon that could tell you?', '2. Art can tell you a lot about a person\'s life...', '3. Examine the art in the Prison.', '4. 1759'], puzzlesList, [lever1, lever7, lever5, lever9],
		'')
	MaizeAndBlue = OrderPuzzle('You see two circular indentations in the Northern wall, the same size as the disks on the table. An inscription on the wall above the indentations says in calligraphy: \
"O, Carleton, our Alma Mater, we hail the _____ and ____.', 'You did it! The Eastern door opens!', ['1. I wonder what Carleton\'s school colors are...', '2. Have you ever listened to the Carleton song?'
		'3. Maize and Blue.'], puzzlesList, [maizeDisk, blueDisk], 'is pressed into one of the indentations in the Northern wall.')
	Frisbro = SingleItemPuzzle('You see a huge orc dressed like a frisbee player in the middle of the room...they\'re way too big for you to fight. You\'ll have to get them out of the way somehow...',
		'The orc chases the frisbee across the room, until....SMACK! They run into a wall, knocking themselves unconscious.', ['1. Maybe you can distract them?', '2. What would distract a frisbee player?',
		'3. Use your frisbee.'], puzzlesList, frisbee)

	'''***ROOMS***'''
	# EnemyRoom params = roomID, roomsDict, directionsDict, description, itemsList, enemy
	# PuzzleRoom params = roomID, roomsDict, directionsDict, description, itemsList, puzzle, lockedDirectionDict, puzzPrizes
	# Shop params = roomsDict, directionsDict, description, shopDict

	firstRoom = BaseRoom('entrance', roomsDict, {'n': 'prison'}, 'A plain, stone room. There is a door to the North. Next to the door, written in red paint, are the words "ENTER IF YOU DARE".', [])
	prisonRoom = EnemyRoom('prison', roomsDict, {'s': 'entrance', 'n': 'levers room', 'e': 'shop'}, 'A dusty old prison. There are cobwebs everywhere. You can see all of the cell doors have broken open... \
There\'s a door to the South and a door to the North. The door to the Shop is to the East.', [art], goblin)
	shop = Shop(roomsDict, {'w': 'prison'}, 'You walk into a shop. There\'s a person working the register in the back...I wonder how long they\'ve been here?', {leatherCap: 2, leatherTunic: 6, leatherLeggings: 4, leatherBoots: 2})
	leversRoom = PuzzleRoom('levers room', roomsDict, {'s': 'prison'}, 'Another normal, basic room. This dungeon must be hundreds of years old... \nThere\'s a door to the South.', [lever0, lever1, lever2, lever3, lever4, lever5, lever6, lever7, lever8, lever9], LeversPuzzle, {'w': 'furnace room'}, [frisbee])
	furnaceRoom = EnemyRoom('furnace room', roomsDict, {'e': 'levers room', 'n': 'color room'}, 'You can see that this used to be where all of the coal was kept because of the dark black stains \
all over the floor. There\'s a door to the East and a door to the North.', [furnace], skeleton)
	colorRoom = PuzzleRoom('color room', roomsDict, {'s': 'furnace room'}, 'This room stands out from every other room. It has bright colors everywhere...it kind of hurts your eyes a little bit... \
There\'s a door to the South.', [table, maizeDisk, greenDisk, redDisk, blueDisk, purpleDisk], MaizeAndBlue, {'e': 'workout room'}, [schillers6])
	workoutRoom = PuzzleRoom('workout room', roomsDict, {'w': 'color room'}, 'Even monsters need to workout sometimes. There\'s a door to the West.', [], Frisbro, {'e': 'laundry room?'}, [KnightHelm])
	laundryRoom = EnemyRoom('laundry room?', roomsDict, {'w': 'workout room', 'n': 'BOSS ROOM'}, 'I guess monsters need to do laundry too? Who knows... There\'s a door to the West and a door to the \
North...you get the feeling that there\'s something dangerous to the North.', [LaundryMaschine], orc)
	bossRoom = EnemyRoom('BOSS ROOM', roomsDict, {'s': 'laundry room?', 'n': 'schiller room'}, 'This room seems to be plated in gold. There\'s a beautiful bejeweled door to the North and another one to the South. You look up and see...', [], dragon)
	schillerRoom = BaseRoom('schiller room', roomsDict, {'s': 'BOSS ROOM'}, 'You\'ve made it at last!', [pedestal, SchillerBust])

	player = Player(firstRoom)

	intro()
	print(player.look())
	playerCommand = input('>')
	while playerCommand not in ['exit', 'quit', '']:
		print(interpret(player, itemsDict, playerCommand))
		print()
		if not player.isAlive():
			print('YOU HAVE DIED.')
			break
		elif SchillerBust in player.inventory:
			print('VICTORY!!!!')
			break
		playerCommand = input('>')
	if playerCommand not in ['exit', 'quit', '']:
		print('Thank you for playing "Carleton College: The Quest for Schiller"! Would you like to play again? (Y/N)')
		response = input('>')
		while response[0].lower() not in ['y', 'n']:
			print("I don't understand. Do you want to play again? (Y/N)")
			response = input('>')
		if response[0].lower() == 'y':
			game()
	print('Goodbye!')

if __name__ == '__main__':
	game()

