import numpy as np
import random

class Card():  # This is the class for each card
    suit = None
    rank = None

    def record_move(self):  # records the state of the piles after each move, saves it in the playbyplay list
        set = []
        for x in range(len(piles)):
            set.append([piles[x][0].rank, piles[x][0].suit])
        playbyplay.append(set)

    def location(self):  # returns the pile number of the card
        for x in range(len(piles)):
            for y in range(len(piles[x])):
                if piles[x][y].suit == self.suit and piles[x][y].rank == self.rank:
                    return x

    def check(self, index):
        if index > 0 and len(piles) > self.location() + abs(index) or index < 0 and len(piles) > -index:
            if self.suit == piles[self.location() + index][0].suit or self.rank == piles[self.location() + index][
                0].rank:
                return True
        return False

    def double_move_one(
            self):  # This checks to see if there is a possibility of a double move, given the drawn card is moved one to the left initially.
        if len(piles) > 2:
            if self.suit == piles[self.location() - 2][0].suit:
                return True
            if self.rank == piles[self.location() - 2][0].rank:
                return True

        if len(piles) > 4:
            if self.suit == piles[self.location() - 4][0].suit:
                return True
            if self.rank == piles[self.location() - 4][0].rank:
                return True
        return False

    def double_move_three(
            self):  # This checks to see if there is a possibility of a double move, given the drawn card is moved three to the left initially.
        if len(piles) > 4:
            if self.suit == piles[self.location() - 4][0].suit:
                return True
            if self.rank == piles[self.location() - 4][0].rank:
                return True

        if len(piles) > 6:
            if self.suit == piles[self.location() - 6][0].suit:
                return True
            if self.rank == piles[self.location() - 6][0].rank:
                return True
        if len(piles) > 2:
            if self.suit == piles[self.location() - 2][0].suit:
                return True
            if self.rank == piles[self.location() - 2][0].rank:
                return True
        return False

    def check_recursively(
            self):  # This function checks the board for possible additional moves after the first card has been moved. It will recursively check for new moves every time it moves a card.
        # The check will stop once no new moves are found.

        golden_list = [3, 1, -1, -3]

        for x in range(4):
            if (golden_list[x] < 0 and abs(golden_list[x]) > self.location()) or (
                            golden_list[x] > 0 and self.location() + golden_list[x] >= len(piles)):
                pass

            else:
                focusindex = piles[self.location() + golden_list[x]][0].location()

                for y in range(4):

                    if (golden_list[y] < 0 and abs(golden_list[y]) > focusindex) or (
                                    golden_list[y] > 0 and focusindex + golden_list[y] > len(piles)):
                        pass
                    else:
                        if piles[focusindex][0].check(golden_list[y]):

                            destinationindex = piles[focusindex + golden_list[y]][0].location()
                            tempindex = focusindex
                            # print("Focus index: %d, Destination index: %d" %(focusindex,destinationindex))

                            if focusindex > destinationindex:
                                piles[destinationindex] = piles[focusindex] + piles[destinationindex]

                                del piles[focusindex]

                                piles[destinationindex][0].check_recursively()
                            else:
                                piles[focusindex] = piles[destinationindex] + piles[focusindex]
                                del piles[destinationindex]
                                piles[focusindex][0].check_recursively()
                            self.record_move()

                            break

    def move_left_one(self):  # moves the drawn card onto the piles immediately to the left

        piles[self.location() - 1].insert(0, self)
        del piles[self.location() + 1]
        self.record_move()

    def move_left_three(self):  # moves the drawn card onto the pile three to the left of it.

        piles[self.location() - 3].insert(0, self)
        if (self.location() + 3) < len(piles):
            del piles[self.location() + 3]
        self.record_move()

    def first_card_check(
            self):  # checks to see if the card can be immediately moved once drawn and put at the end of the piles. Gives preference to moves that allow for subsequent moves
        if self.check(-1) and not self.check(-3):
            self.move_left_one()

            self.check_recursively()

        if self.check(-3) and not self.check(-1):
            self.move_left_three()

            self.check_recursively()
        if self.check(-1) and self.check(-3):
            if self.double_move_one() and not self.double_move_three():
                self.move_left_one()

                self.check_recursively()
            if self.double_move_three() and not self.double_move_one():
                self.move_left_three()

                self.check_recursively()

            else:
                self.move_left_one()
                # insert some code to check outs and determine best moves

                self.check_recursively()

class Deck:  # each deck is its own class
    card_list = []
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def make_cards(self):  # Deck.card_list is a list of all 52 cards
        for s in range(len(self.suits)):
            for x in range(len(self.ranks)):
                self.card_list.append(Card())
                self.card_list[-1].rank = self.ranks[x]
                self.card_list[-1].suit = self.suits[s]

    def shuffle(self):  # Shuffles the deck in place
        random.shuffle(self.card_list)

    def riffle(self):
        inds = list(range(52))
        cut_loc = int(np.round(np.random.normal(loc=26.0, scale=4.0)))
        if cut_loc < 1: cut_loc = 1
        elif cut_loc > 51: cut_loc = 51
        top = inds[:cut_loc]
        bot = inds[cut_loc:]
        p_top = 0.5
        new_inds = []
        while len(top) > 0 or len(bot) > 0:
            rand = np.random.rand()
            if rand > p_top and len(top) > 0:
                new_inds.append(top.pop())
                p_top = 0.9
            elif rand < p_top and len(bot) > 0:
                new_inds.append(bot.pop())
                p_top = 0.1
            elif len(top) == 0:
                new_inds.append(bot.pop())
            elif len(bot) == 0:
                new_inds.append(top.pop())
        new_inds = np.array(new_inds, dtype=np.int)
        self.card_list = [self.card_list[i] for i in new_inds]

    def cut(self):
        inds = range(52)
        cut_loc = np.round(np.random.normal(loc=26.0, scale=10.0))
        if cut_loc < 1: cut_loc = 1
        elif cut_loc > 51: cut_loc = 51

    def draw(self):  # Draws the first card from the deck and returns it
        temp_card = self.card_list[0]
        del self.card_list[0]
        return (temp_card)


def game_loop(init_deck=None, riffles=0):  # all of the classes and methods needed to play the game are enclosed in a game loop to allow for multiple games to be played.
    
    if init_deck == None:
        mydeck = Deck()  # Creates a deck to be used during the game

        mydeck.make_cards()  # Makes an object instance of the Card class 52 times

        mydeck.shuffle()

    else:
        mydeck = Deck()
        mydeck.card_list = init_deck
        for i in range(riffles):
            mydeck.riffle()

    global piles
    piles = []  # These are the piles you lay down on the table when you are playing the game
    global decklist  # This is the list of cards that have been played already. It is used to determine probabilies about the next card to be drawn
    decklist = []
    global playbyplay  # This is a list of the piles after every move
    playbyplay = []

    for i in range(52):
        card = mydeck.draw()
        decklist.append([card.rank, card.suit])
        # print(card.rank,card.suit)

        piles.append([card])
        card.record_move()
        # print(piles[-1][0].rank,piles[-1][0].suit)

        card.first_card_check()

    global endpiles
    endpiles = []

    for x in range(len(piles)):
        endpiles.append([piles[x][0].rank, piles[x][0].suit])
    return piles


# will continue to play games until it wins max_wins number of times
# prints the number of games played before each win
def play_to_win(max_wins, riffles=None):
    stats = []

    num_wins = 0
    
    final_piles = []
    all_gamesplayed = []
    while num_wins < max_wins:
        win = False
        if riffles == None:
            first_deck = Deck()  # Creates a deck to be used during the game
            first_deck.make_cards()  # Makes an object instance of the Card class 52 times
            first_deck.shuffle()
            final_pile = [first_deck.card_list]

        while not win:
            if riffles == None:
                prev_deck = []
                for sublist in final_pile:
                    for item in sublist:
                        prev_deck.append(item)
                final_pile = game_loop(init_deck=prev_deck, riffles=riffles)
                final_piles.append(final_pile)
                stats.append(len(endpiles))
                stats.sort()
            else:
                final_pile = game_loop()
                final_piles.append(final_pile)
                stats.append(len(endpiles))
                stats.sort()
                
            if stats[0] == 1:
                win = True
                num_wins += 1

                global gamesplayed
                gamesplayed = len(stats)
                stats = []
                piles = []
                # print("Play by play of winning game:\n")
                # for play in playbyplay:
                # for pile in play:
                # print(pile)
                # print("\n")
                print(f"Number of games played before win: {gamesplayed}")
                all_gamesplayed.append(gamesplayed)
    return final_piles, all_gamesplayed


for i in range(4):
    print(f"\n\nPlaying with {i+8} riffle shuffles:")
    final_piles, gamesplayed = play_to_win(50, riffles=i+8)

    num_stacks = []
    for final_pile in final_piles:
        num_stacks.append(len(final_pile))

    num_stacks = np.array(num_stacks)
    np.save(f"stack_distribution_{i+8}_riffle.npy", num_stacks)
    np.save(f"gamesplayed_{i+1}_riffle.npy", gamesplayed)
