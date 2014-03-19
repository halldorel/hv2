import deck as d
import unittest

class RuleMethods(unittest.TestCase):
	# Tests GameState.can_discard()
	def testDiscardCard(self):
		game = d.GameState()
		# We create an instance where we should be able to discard
		# a single card from the table.
		game.table[0].place(d.Card(2, 'H'))
		game.table[1].place(d.Card(3, 'H'))
		game.table[2].place(d.Card(3, 'S'))
		game.table[3].place(d.Card(3, 'C'))
		self.assertTrue(game.can_discard(game.table[0].top(), 0))
		self.assertFalse(game.can_discard(game.table[1].top(), 1))
		# We create an instance where no card can be discarded.
		game.table[0].place(d.Card(4, 'D'))
		game.table[1].place(d.Card(5, 'H'))
		game.table[2].place(d.Card(6, 'S'))
		game.table[3].place(d.Card(7, 'C'))
		for i in range(4):
			self.assertFalse(game.can_discard(game.table[i].top(), i))

class DeckMethods(unittest.TestCase):
	# Tests GameState.top()
	def testTop(self):
		game = d.GameState()
		card = d.Card(2, 'H')
		game.table[0].place(card)
		self.assertTrue(game.table[0].top().suit == card.suit)
		self.assertTrue(game.table[0].top().rank == card.rank)

	# Tests the overloaded __cmp__() function for Card
	def testCardCmp(self):
		card1 = d.Card(2, 'H')
		card2 = d.Card(2, 'C')
		self.assertTrue(card1 == card2)
		card2 = d.Card(3, 'C')
		self.assertTrue(card1 < card2)
		self.assertFalse(card1 > card2)

	# Tests Card.suit_buddies()
	def testSuitBuddies(self):
		card1 = d.Card(2, 'H')
		card2 = d.Card(3, 'H')
		self.assertTrue(card1.suit_buddies(card2))
		card2 = d.Card(2, 'C')
		self.assertFalse(card1.suit_buddies(card2))

class DeckLegal(unittest.TestCase):
	# Tests whether deck contains duplicate cards
	def testDuplicates(self):
		game = d.GameState()
		deck = game.deck.deck

		while len(deck) != 0:
			card = deck.pop()
			for c in deck:
				self.assertFalse(card.suit == c.suit and card.rank == c.rank)

class testUI(unittest.TestCase):
	# UI state tests
	def testTopCardIsDraggable(self):
		game = d.GameState()
		game.draw()
		game.draw()
		is_draggable = game.table[0].top().draggable
		self.assertTrue(is_draggable)
 
	def testCardBelowIsNotDraggable(self):
		game = d.GameState()
		game.draw()
		game.draw()
		is_draggable = game.table[0].deck[-2].draggable
		self.assertFalse(is_draggable)


if __name__ == "__main__":
	unittest.main() 