
def gameloop():
	import random

	class Card(): #This is the class for each card
			suit = None
			rank = None

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

			def double_move_one(self):
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

			def double_move_three(self):
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

			def supercheck(self):
					
					goldenlist = [-3,-1,1,3]

					for x in range(4):
							if (goldenlist[x] < 0 and abs(goldenlist[x]) > self.location()) or (goldenlist[x] > 0 and self.location() + goldenlist[x] >= len(piles)):
									pass

							else:
									focuspile = piles[self.location() + goldenlist[x]]
									
									for y in range(4):
											




											if (goldenlist[y] < 0 and abs(goldenlist[y]) > focuspile[0].location()) or (goldenlist[y] > 0 and focuspile[0].location() + goldenlist[y] > len(piles)):
													pass
											else:
												if focuspile[0].check(goldenlist[y]):
														
														focuspile = piles[focuspile[0].location() + goldenlist[y]] + focuspile
														
														del piles[focuspile[0].location()-goldenlist[y]]
														
														card.supercheck()
														break




			def move_left_one(self):
				piles[self.location()-1].insert(0,self)
				del piles[self.location()+1]				



			def move_left_three(self):
				piles[self.location()-3].insert(0,self)
				del piles[self.location()+3]


			def first_card_check(self):
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

			def shuffle(self):
					random.shuffle(self.card_list)

			def draw(self):
					tempcard	= self.card_list[0]
					del self.card_list[0]
					return (tempcard)

				
	mydeck = Deck()

	mydeck.make_cards()
	
	mydeck.shuffle()
	
	piles = []

	for i in range(52):
		card = mydeck.draw()
					#print(card.rank,card.suit)

		piles.append([card])
					#print(piles[-1][0].rank,piles[-1][0].suit)

		card.first_card_check()

	global endpiles
	endpiles = []
	for x in range(len(piles)):

		endpiles.append([piles[x][0].rank,piles[x][0].suit])
	#print("Final Piles:\n",endpiles)
	#print("Final Number of Piles:\n",len(endpiles))
	#print(2*"\n")


def playtowin(): #will continue to play games until it wins, prints the number of games played before win

	stats = []
	win = False
	while win == False:
		gameloop()
		stats.append(len(endpiles))
		stats.sort()
		if stats[0] == 1:
			win = True
			global gamesplayed
			gamesplayed = len(stats)
			print("You win!")
			print("Number of games played before win:",gamesplayed,"\n")
			
playtowin()

