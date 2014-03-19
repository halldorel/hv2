import pygame

# Constants:
# ============================
# Number of decks on table:
NUM_DECKS = 4

# TODO: Convert BJORUNDUR to a global plugin
BJORUNDUR = pygame.image.load('img/bjorundur.png')
STEINI = pygame.image.load('img/steini_king_card.png')


class Card:
	def __init__(self, rank, suit, pos=(0,0), draggable=True):
		self.rank = rank
		self.suit = suit

		# Position of card within playing field
		self.pos = pos

		# TODO: Remove hardcoded values and read them from image
		self.size = (135, 195)
		self.rect = pygame.Rect(self.pos, self.size)
		self.surf = pygame.Surface(self.size, pygame.SRCALPHA, 32)

		# Font shitmix
		# TODO: remove
		self.font = pygame.font.SysFont('Comic Sans MS', 20)
		self.textsurf = self.font.render(str(self), True, (0, 0, 0))
		self.surf.blit(STEINI,(0,0))
		self.surf.blit(self.textsurf, (50, 50))

		self.draggable = draggable
		if self.rank == 0 or self.suit == 0:
			self.draggable = False

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

	# Set image position and rectangle at given pos
	def set_pos(self, pos):
		self.pos = pos
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	def set_draggable(self):
		self.draggable = True

	def set_undraggable(self):
		self.draggable = False
		print " Set undraggable: " + str(self)

	def is_draggable(self):
		return self.draggable

	def is_dummy(self):
		return self.rank == 0 and self.suit == 0

	# Nudge card position
	# delta should be a tuple
	def nudge(self, delta):
		curr_pos = self.pos
		# Incredible shitmix for adding tuples discretely
		# Probably very slow and bad for pandas :-(
		next_pos = tuple(map(sum, zip(curr_pos, delta)))
		self.set_pos(next_pos)

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
		self.base = Card(0, 0, self.pos)

	# Returns top card, or a dummy empty card which represents base of table
	def top(self):
		if not self.is_empty():
			return self.deck[-1]
		else:
			return self.base

	def pop(self):
		popped = self.deck.pop()
		top = self.top()
		if top:
			top.set_draggable()
		return popped

	def place(self, card):
		# Make current top card undraggable
		if not self.is_empty():
			self.top().set_undraggable()
		# Calculate position of new card from next index in this Table
		next_index = len(self.deck)
		card_x = self.pos[0]
		card_y = self.pos[1] + next_index * self.STACK_STRIDE

		# Set the position of the card
		card.set_pos((card_x, card_y))

		self.deck.append(card)
		self.top().set_draggable()

	def get_deck(self):
		return self.deck

	def render(self, screen):
		if self.deck:
			for i, card in enumerate(self.deck):
				at = tuple(map(sum, zip(self.pos, (0, self.STACK_STRIDE*i))))
				card.render(screen)
		else:
			screen.blit(BJORUNDUR, self.pos)

class Stack(Deck):
	def __init__(self, pos, ranks = range(1, 14), suits=['H', 'S', 'D', 'C']):
		self.deck = [Card(rank, suit, pos, draggable=True) for rank in ranks for suit in suits]
		self.pos = pos
		self.base = Card(0, 0, self.pos)

	def draw(self):
		return [self.deck.pop() for i in range(NUM_DECKS)]

	def get_rect(self):
		if not self.is_empty():
			return self.deck[-1].rect
		return pygame.rect(0, 0, 0, 0)

	def get_base(self):
		return self.base

	def render(self, screen):
		if not self.is_empty():
			screen.blit(BJORUNDUR, self.pos)

class Game:
	def __init__(self):
		# TODO: Shuffle the deck! Otherwise gameplay is boring
		self.deck = Stack((40, 50))
		self.table = [Table((250 + 155*i, 50)) for i in range(NUM_DECKS)]
		self.trash = Table((900, 460))
		self.card_being_dragged = None

	def draw(self):
		if not self.deck.is_empty():
			hand = self.deck.draw()
			for i in range(NUM_DECKS):
				self.table[i].place(hand[i])

	def start_dragging(self, card):
		self.card_being_dragged = card

	def stop_dragging(self, card):
		self.card_being_dragged = None

	# Determine which table to drop to.
	def which_table(self, card):
		# Card can be dropped on many cards. Get largest intersection.
		collisions = []

		for table in self.table:
			top_card = table.top()
			# Get the intersection rectangle
			collisions.append(top_card.rect.clip(card))

		# See which table's top card dragged card covers the most
		rect_area_max = 0
		table = None
		for i, collision in enumerate(collisions):
			rect_area = collision.width * collision.height
			if rect_area > rect_area_max:
				rect_area_max = rect_area
				table = self.table[i]
		return table

	def handle_card_dropped(self, card):
		# TODO: Insert game logic, check if the move is legal
		table = self.which_table(card)
		# If card is dropped on any table, place card there
		if table:
			table.place(card)
			return True
		# Otherwise, return to original table
		else:
			return False

	# Check which card is pressed. Returns None if no card is pressed.
	# Also return table

	def handle_draw(self, mouse_pos):
		if not self.deck.is_empty():
			deck_rect = self.deck.get_rect()
			if deck_rect.collidepoint(mouse_pos):
				self.draw()
	
	def card_pressed(self, mouse_pos):
		# Check if user wants to deal cards 
		for table in self.table:
			for i, card in enumerate(table.get_deck()):
				if card.rect.collidepoint(mouse_pos) and card.is_draggable():
					return (card, table)
		return None

	def render(self, screen):
		# Render deck
		self.deck.render(screen)
		for table in self.table:
			table.render(screen)
		self.trash.render(screen)

