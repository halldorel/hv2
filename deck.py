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
	deck = []

	@property
	def STACK_STRIDE(self):
		return 20

	def is_empty(self):
		return len(self.deck) == 0

	def get_pos(self):
		return self.pos;
	
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
	def __init__(self, pos, ranks = range(1, 14), suits = ['H', 'S', 'D', 'C']):
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
	def __init__(self, screen):
		# TODO: Shuffle the deck! Otherwise gameplay is boring
		self.background_color = (80, 170, 80)
		self.screen = screen
		self.deck = Stack((40, 50))
		self.table = [Table((250 + 155*i, 50)) for i in range(NUM_DECKS)]
		self.trash = Table((900, 460))
		self.running = True
		self.current_card = None
		self.last_table = None
		self.BJORUNDUR = pygame.image.load('bjorundur.png')

	def draw(self):
		if not self.deck.is_empty():
			hand = self.deck.draw()
			for i in range(NUM_DECKS):
				self.table[i].place(hand[i])

	# TODO: Function for ending game, that is setting self.running to False

	# Determine which table to drop to according to collision area size.
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

	def update(self):
		# Each time, we draw all the components of the screen, beginning
		# with the background. We draw the background by filling the 'screen'
		# surface with a solid color.
	
		# Loop through the event queue to check what's happening.
		for event in pygame.event.get():
			# Mouse event variables.
			mouse_buttons = pygame.mouse.get_pressed()
			mouse_delta = pygame.mouse.get_rel()
			mouse_pos = pygame.mouse.get_pos()
		
			# Voluntary quit
			if event.type == pygame.QUIT:
				self.running = False	
	
			# Release the card if currently held, when releasing the mouse
			if event.type == pygame.MOUSEBUTTONUP:
				if self.current_card and self.last_table:
					if not self.handle_card_dropped(self.current_card):
						self.last_table.place(self.current_card)
					self.current_card = None
					
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.handle_draw(mouse_pos)
	
			# If left mouse button is pressed, check if we're holding a card
			# if not, holding a card, set self.current_card to the card pressed
			if mouse_buttons == (1, 0, 0):
				if not self.current_card:
					if self.card_pressed(mouse_pos):
						(self.current_card, self.last_table) = self.card_pressed(mouse_pos)
						if self.current_card and self.last_table:
							self.current_card = self.last_table.top()
							self.last_table.pop();
				else:
					self.current_card.nudge(mouse_delta)

	def render(self):
		# Render deck
		self.screen.fill(self.background_color)
		self.deck.render(self.screen)
		for table in self.table:
			table.render(self.screen)
		self.trash.render(self.screen)

		if self.current_card and not self.current_card.is_dummy():
			self.current_card.render(self.screen)

		# Update the screen.
		pygame.time.delay(16)
		pygame.display.flip()

	def play(self):
		while self.running:
			self.update()
			self.render()