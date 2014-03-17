# Constants:
# ============================
# Number of decks on table:
NUM_DECKS = 4

class Card:
	def __init__(rank, suit):
		self.rank = rank
		self.suit = suit

	# Returns true if the self is of the same suit as other
	def __eq__(self, other):
		return self.suit == other.suit

	# ans < 0 if self.rank < other.rank
	# ans == 0, if self.rank == other.rank
	# ans > 0, if self.rank > other.rank
	def __cmp__(self, other):
		return self.rank - other.rank


class Deck:
	def isEmpty(self):
		return len(self.deck == 0)


	


class Table(Deck):
	def __init__(self):
		self.deck = []

	def top(self):
		if not self.isEmpty():
			return self.deck[-1]

	def place(self, card):
		self.deck.append(card)


class Stack(Deck):
	def __init__(self, ranks = range(1, 14), suits=['H', 'S', 'D', 'C']):
		self.deck = [card(rank, suit) for rank in ranks for suit in suits]

	def draw(self):
		return [self.deck.pop() for i in range(NUM_DECKS)]


class Game:
	def __init__(self):
		self.deck = Stack()
		self.table = [Table() for i in range(NUM_DECKS)]
		self.trash = Table()

	def draw(self):
		hand = self.deck.draw()
		for i in range(NUM_DECKS):
			self.table[i].place(hand[i])
