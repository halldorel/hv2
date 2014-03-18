import pygame

# Constants:
# ============================
# Number of decks on table:
NUM_DECKS = 4

# TODO: Convert BJORUNDUR to a global plugin
BJORUNDUR = pygame.image.load('bjorundur.png')
STEINI = pygame.image.load('img/steini_king_card.png')


class Card:
	def __init__(self, rank, suit, pos=(0,0), draggable=True):
		self.rank = rank
		self.suit = suit

		self.pos = pos
		self.size = (135, 195)
		self.rect = pygame.Rect(self.pos, self.size)

		self.surf = pygame.Surface(self.size, pygame.SRCALPHA, 32)

		# Font shitmix
		self.font = pygame.font.SysFont('Comic Sans MS', 20)
		self.textsurf = self.font.render(str(self), True, (0, 0, 0))
		self.surf.blit(STEINI,(0,0))
		self.surf.blit(self.textsurf, (50, 50))

		self.draggable = draggable
		#self.surf.blit(BJORUNDUR, (0,0))

	# Returns true if the self is of the same suit as other
	def __eq__(self, other):
		return self.suit == other.suit

	# ans < 0 if self.rank < other.rank
	# ans == 0, if self.rank == other.rank
	# ans > 0, if self.rank > other.rank
	def __cmp__(self, other):
		return self.rank - other.rank

	def __repr__(self):
		return "[" + str(self.rank) + " " + str(self.suit) + "]"

	def render(self, screen):
		screen.blit(self.surf, self.pos)

	def set_pos(self, pos):
		self.pos = pos
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	def set_draggable(self):
		self.draggable = True

	def set_undraggable(self):
		self.draggable = False

	def is_draggable(self):
		return self.draggable

	def nudge(self, delta):
		self.pos = (self.pos[0] + delta[0], self.pos[1] + delta[1])
		self.rect = pygame.Rect(self.pos, self.size)

	def set_x(self, x):
		self.pos = (x, self.pos[1])


class Deck:
	# Top spacing between cards in a stack 
	@property
	def STACK_STRIDE(self):
		return 20

	def is_empty(self):
		return len(self.deck) == 0
	

class Table(Deck):
	def __init__(self, pos):
		self.deck = []
		self.pos = pos

	def top(self):
		if not self.is_empty():
			return self.deck[-1]

	def place(self, card):
		# Make current top card undraggable
		if not self.is_empty():
			self.deck[-1].set_undraggable()
		# Calculate position of new card from next index in this Table
		next_index = len(self.deck)
		card_x = self.pos[0]
		card_y = next_index * self.STACK_STRIDE

		# Set the position of the card
		card.set_pos((card_x, card_y))

		# Debug output
		print "card: " + str(card) + " at: " + str(card_x) + ", "  + str(card_y)
		self.deck.append(card)

	def get_deck(self):
		return self.deck

	def render(self, screen):
		if self.deck:
			for i, card in enumerate(self.deck):
				at = self.pos + (0, self.STACK_STRIDE*i)
				card.render(screen)
		else:
			screen.blit(BJORUNDUR, self.pos)

class Stack(Deck):
	def __init__(self, pos, ranks = range(1, 14), suits=['H', 'S', 'D', 'C']):
		self.deck = [Card(rank, suit, pos, draggable=True) for rank in ranks for suit in suits]
		self.pos = pos

	def draw(self):
		return [self.deck.pop() for i in range(NUM_DECKS)]

	def render(self, screen):
		if self.deck:
			screen.blit(BJORUNDUR, self.pos)

class Game:
	def __init__(self):
		self.deck = Stack((300, 300))
		self.table = [Table((20 + 180*i, 20 + 100)) for i in range(NUM_DECKS)]
		self.trash = Table((800, 100))

	def draw(self):
		hand = self.deck.draw()
		for i in range(NUM_DECKS):
			self.table[i].place(hand[i])

	# Check which card is pressed. Returns None if no card is pressed.
	def card_pressed(self, mouse_pos):
		# Search for card in reversed list. Cards appearing later in list
		# have precedence as they are rendered last and thus appear on top.
		for table in self.table:
			for card in table.get_deck()[::-1]:
				if card.rect.collidepoint(mouse_pos):# and card.is_draggable():
					print card
					return card
		return None

	def render(self, screen):
		# Render deck
		self.deck.render(screen)
		for table in self.table:
			table.render(screen)
		self.trash.render(screen)

