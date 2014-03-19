import deck
import unittest

class RuleMethods(unittest.TestCase):
	def testDiscardCard(self):
		game = deck.Game()
		# We create an instance where we should be able to discard
		# a single card from the table.
		game.table[0].place(deck.Card(2, 'H'))
		game.table[1].place(deck.Card(3, 'H'))
		game.table[2].place(deck.Card(3, 'S'))
		game.table[3].place(deck.Card(3, 'C'))
		self.assertTrue(game.can_discard(game.table[0].top(), 0))
		self.assertFalse(game.can_discard(game.table[1].top(), 1))
		# We create an instance where no card can be discarded.
		game.table[0].place(deck.Card(4, 'D'))
		game.table[1].place(deck.Card(5, 'H'))
		game.table[2].place(deck.Card(6, 'S'))
		game.table[3].place(deck.Card(7, 'C'))
		for i in range(4):
			self.assertFalse(game.can_discard(game.table[i].top(), i))

if __name__ == "__main__":
	unittest.main() 