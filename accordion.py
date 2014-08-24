
def gameloop(): #all of the classes and methods needed to play the game are enclosed in a game loop to allow for multiple games to be played.
	import random

	class Card(): #This is the class for each card
			suit = None
			rank = None
			
			def recordmove(self): # records the state of the piles after each move, saves it in the playbyplay list
				set = []
				for x in range(len(piles)):
					set.append([piles[x][0].rank,piles[x][0].suit])
				playbyplay.append(set)			

			def location(self): #returns the pile number of the card
					for x in range(len(piles)):
							for y in range(len(piles[x])):
									if piles[x][y].suit == self.suit and piles[x][y].rank == self.rank:
											return x

			def check(self,index):
					if index > 0 and len(piles) > self.location()+abs(index) or index <0 and len(piles) > -index:
							if self.suit == piles[self.location()+index][0].suit or self.rank == piles[self.location()+index][0].rank:
									return True
					return False

			def double_move_one(self): #This checks to see if there is a possibility of a double move, given the drawn card is moved one to the left initially.
					if len(piles) > 2:
							if self.suit == piles[self.location()-2][0].suit:
									return True
							if self.rank == piles[self.location()-2][0].rank:
									return True

					if len(piles) > 4:
							if self.suit == piles[self.location()-4][0].suit:
									return True
							if self.rank == piles[self.location()-4][0].rank:
									return True
					return False

			def double_move_three(self): #This checks to see if there is a possibility of a double move, given the drawn card is moved three to the left initially.
					if len(piles) > 4:
							if self.suit == piles[self.location()-4][0].suit:
									return True
							if self.rank == piles[self.location()-4][0].rank:
									return True

					if len(piles) > 6:
							if self.suit == piles[self.location()-6][0].suit:
									return True
							if self.rank == piles[self.location()-6][0].rank:
									return True
					if len(piles) > 2:
							if self.suit == piles[self.location()-2][0].suit:
									return True
							if self.rank == piles[self.location()-2][0].rank:
									return True
					return False

			def supercheck(self): #This function checks the board for possible additional moves after the first card has been moved. It will recursively check for new moves every time it moves a card.
								# The check will stop once no new moves are found.
					
					goldenlist = [3,1,-1,-3]

					for x in range(4):
							if (goldenlist[x] < 0 and abs(goldenlist[x]) > self.location()) or (goldenlist[x] > 0 and self.location() + goldenlist[x] >= len(piles)):
									pass

							else:
									focusindex = piles[self.location() + goldenlist[x]][0].location()
									
									for y in range(4):
											




											if (goldenlist[y] < 0 and abs(goldenlist[y]) > focusindex) or (goldenlist[y] > 0 and focusindex + goldenlist[y] > len(piles)):
													pass
											else:
												if piles[focusindex][0].check(goldenlist[y]):
														
														
														
														destinationindex = piles[focusindex + goldenlist[y]][0].location()
														tempindex = focusindex
														#print("Focus index: %d, Destination index: %d" %(focusindex,destinationindex))
														
														
														if focusindex > destinationindex:
															piles[destinationindex] = piles[focusindex] + piles[destinationindex]


															del piles[focusindex]
															
															piles[destinationindex][0].supercheck()
														else:
															piles[focusindex] = piles[destinationindex] + piles[focusindex]
															del piles[destinationindex]
															piles[focusindex][0].supercheck()
														self.recordmove()
														
														
														
														break




			def move_left_one(self): # moves the drawn card onto the piles immediately to the left
				
				piles[self.location()-1].insert(0,self)
				del piles[self.location()+1]
				self.recordmove()



			def move_left_three(self): # moves the drawn card onto the pile three to the left of it.
				
				piles[self.location()-3].insert(0,self)
				del piles[self.location()+3]
				self.recordmove()


			def first_card_check(self): #checks to see if the card can be immediately moved once drawn and put at the end of the piles. Gives preference to moves that allow for subsequent moves
					if self.check(-1) and not self.check(-3):
							self.move_left_one()

							self.supercheck()

					if self.check(-3) and not self.check(-1):
							self.move_left_three()

							self.supercheck()
					if self.check(-1) and self.check(-3):
							if self.double_move_one() and not self.double_move_three():
									self.move_left_one()

									self.supercheck()
							if self.double_move_three() and not self.double_move_one():
									self.move_left_three()

									self.supercheck()

							else:
									self.move_left_one()
									#insert some code to check outs and determine best moves

									self.supercheck()		

	class Deck(): #each deck is its own class
			card_list = []
			suits = ["Hearts","Diamonds","Clubs","Spades"]
			ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

			def make_cards(self): #Deck.card_list is a list of all 52 cards
					for s in range(len(self.suits)):
							for x in range(len(self.ranks)):

									self.card_list.append(Card())
									self.card_list[-1].rank = self.ranks[x]
									self.card_list[-1].suit =self.suits[s]

			def shuffle(self): # Shuffles the deck in place
					random.shuffle(self.card_list)

			def draw(self): # Draws the first card from the deck and returns it
					tempcard	= self.card_list[0]
					del self.card_list[0]
					return (tempcard)

				
	mydeck = Deck() #Creates a deck to be used during the game

	mydeck.make_cards() # Makes an object instance of the Card class 52 times
	
	mydeck.shuffle()
	
	piles = [] # These are the piles you lay down on the table when you are playing the game
	global decklist # This is the list of cards that have been played already. It is used to determine probabilies about the next card to be drawn
	decklist = []
	global playbyplay # This is a list of the piles after every move
	playbyplay = []

	for i in range(52):
		card = mydeck.draw()
		decklist.append([card.rank,card.suit])
					#print(card.rank,card.suit)

		piles.append([card])
		card.recordmove()
					#print(piles[-1][0].rank,piles[-1][0].suit)

		card.first_card_check()
	

	global endpiles
	endpiles = []
	
	for x in range(len(piles)):

		endpiles.append([piles[x][0].rank,piles[x][0].suit])
		
	


def playtowin(max_wins): #will continue to play games until it wins max_wins number of times, prints the number of games played before each win

	stats = []
	
	num_wins = 0
	#
	while num_wins < max_wins:
		win = False
		while win == False:
			gameloop()
			stats.append(len(endpiles))
			stats.sort()
			if stats[0] == 1:
				win = True
				num_wins +=1

				global gamesplayed
				gamesplayed = len(stats)
				stats = []
				print("You win!")


				print("Play by play of winning game:\n")
				for play in playbyplay:
					for pile in play:
						print(pile)
					print("\n")
				print("Number of games played before win:",gamesplayed,"\n")	
			

			
playtowin(1)	



