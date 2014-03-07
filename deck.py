from card import *
from random import shuffle

class deck:
	def __init__(self):
		self.deck = [(card(suit, rank)) for suit in ["H", "S", "T", "L"] for rank in range(1,14)]

	def __repr__(self):
		return str(self.deck)

	def __len__(self):
		return len(self.deck)

	def shuffle(self):
		shuffle(self.deck)

	def draw(self):
		if len(self.deck) > 0:
			return self.deck.pop(0)