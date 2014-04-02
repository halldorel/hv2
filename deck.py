import pygame
import random
import math

# Constants:
# ============================
# Number of decks on table:
NUM_DECKS = 4

# TODO: Convert BJORUNDUR to a global plugin
BJORUNDUR = pygame.image.load('img/bjorundur.png')
CARD_BASE = pygame.image.load('img/card_base.png')
CARD_SORTS = pygame.image.load('img/icons_sprite.png')
CARD_WIDTH = CARD_BASE.get_rect().width
CARD_HEIGHT = CARD_BASE.get_rect().height

# Mandatory pygame-specific setup
pygame.font.init()

#Pygame does not render newline characters so many strings.
rules =	["The game is about comparing the cards",
		"that are on the top of each pile. When",
		"two cards have the same suit, the user",
		"removes the one of the lower rank by",
		"clicking it. Any card can be moved to",
		"an empty space. When no more cards",
		"can be removed, the deck in the left",
		"corner is clicked and deals four more",
		"cards. Ace is considered to be the",
		"highest rank and the player has won",
		"the game when the table consists of",
		"nothing but the four aces, each in it's",
		"own place."]

winning_status = ["Congratulations! You have won the game.",
				  "Do you want to start a new one?"]

defeat_status = ["Sorry. There are no more legal moves.",
				"Do you want to start a new game?"]				  		

def distSq(a, b):
	return pow(a[0]-b[0], 2) + pow(a[1]-b[1], 2)

class Card:
	EASE_EPS = 0.01
	INTERPOLATE_SPEED = 2
	DROP_SPEED = 2
	def __init__(self, rank, suit, pos=(0,0), draggable=True):
		self.rank = rank
		self.suit = suit

		# Tuple: position of card within playing field
		self.pos = pos
		self.dest = pos

		self.is_held = False
		self.is_easing = False

		# TODO: Remove hardcoded values and read them from image
		self.size = (CARD_WIDTH, CARD_HEIGHT)
		self.rect = pygame.Rect(self.pos, self.size)
		self.surf = pygame.Surface(self.size, pygame.SRCALPHA, 32)
		self.draggable = draggable
		if self.rank == 0 or self.suit == 0:
			self.draggable = False
		if not self.is_dummy():
			self.make_card_surface();

	def make_card_surface(self):
		card_names = ['A', '2', '3', '4', '5', '6',
		'7', '8', '9', '10', 'J', 'Q', 'K']
		suits_to_offset = {
			'C' : 0,
			'S' : 1,
			'D' : 2,
			'H' : 3 }
		if not self.is_dummy():
			font = pygame.font.Font('assets/clarendon.ttf', 22)
			font_rank = font.render(str(card_names[self.rank-1]), True, (0, 0, 0))
			suit_img = pygame.Surface((30, 30), pygame.SRCALPHA, 32)
			suit_img.blit(CARD_SORTS, ((-36*suits_to_offset[self.suit]), 0))
	
			# Lots of hardcoded values to get the layout right
			self.surf.blit(CARD_BASE,(0,0))
			self.surf.blit(font_rank, (25-font_rank.get_rect().width/2,10))
			self.surf.blit(pygame.transform.rotate(font_rank, 180), (CARD_WIDTH-25-font_rank.get_rect().width/2, CARD_HEIGHT-35))
			self.surf.blit(pygame.transform.smoothscale(suit_img, (20, 20)), (16, 40))

	# ans < 0 if self.rank < other.rank
	# ans == 0, if self.rank == other.rank
	# ans > 0, if self.rank > other.rank
	def __cmp__(self, other):
		if self.rank == 1:
			return 1
		if other.rank == 1:
			return -1
		return self.rank - other.rank

	def __repr__(self):
		return "[" + str(self.rank) + " " + str(self.suit) + "]"

	# Returns true if the self is of the same suit as other
	def suit_buddies(self, other):
		return self.suit == other.suit

	def should_ease(self):
		if not self.is_held and abs(self.pos[0] - self.dest[0]) < Card.EASE_EPS and abs(self.pos[1] - self.dest[1]) < Card.EASE_EPS:
			return False
		return True

	def ease(self):
		speed = Card.INTERPOLATE_SPEED
		if not self.is_held:
			speed = Card.DROP_SPEED
		x = int(self.dest[0] - (self.dest[0] - self.pos[0])/speed)
		y = int(self.dest[1] - (self.dest[1] - self.pos[1])/speed)
		self.pos = (x, y)
		self.rect.x = x
		self.rect.y = y

	def update(self):
		if self.should_ease():
			self.ease()
			self.is_easing = True
		else:
			self.is_easing = False

	def render(self, screen):
		screen.blit(self.surf, self.pos)

	# Set image position and rectangle at given pos
	def set_pos(self, pos):
		self.pos = pos
		self.dest = pos

	def set_dest(self, dest):
		self.dest = dest

	def set_draggable(self):
		self.draggable = True

	def set_undraggable(self):
		self.draggable = False

	def is_draggable(self):
		return self.draggable

	def is_dummy(self):
		return self.rank == 0 and self.suit == 0

	# Nudge card position
	# delta should be a tuple of coordinates
	def nudge(self, delta):
		curr_pos = self.pos
		# Incredible shitmix for adding tuples discretely
		# Probably very slow and bad for pandas :-(
		next_pos = tuple(map(sum, zip(curr_pos, delta)))
		self.set_pos(next_pos)

	def set_rand_dest(self):
		x = random.randint(0, screen.width)
		y = random.randint(0, screen.height)
		self.set_dest((x, y))

class Deck:
	# Top spacing between cards in a stack
	#deck = []

	@property
	def STACK_STRIDE(self):
		return 45

	def set_deck(self, deck):
		self.deck = deck

	def is_empty(self):
		return len(self.deck) == 0

	def get_pos(self):
		return self.pos;

	# Returns top card, or a dummy empty card which represents base of table
	def top(self):
		if not self.is_empty():
			return self.deck[-1]
		else:
			return self.base
	
class Table(Deck):
	def __init__(self, pos):
		self.deck = []
		self.pos = pos
		self.base = Card(0, 0, self.pos)

	def pop(self):
		popped = self.deck.pop()
		popped.is_held = True
		top = self.top()
		if top:
			top.set_draggable()
		return popped

	def is_empty(self):
		return len(self.deck) == 0

	def place(self, card):
		# Make current top card undraggable
		if not self.is_empty():
			self.top().set_undraggable()
		# Calculate position of new card from next index in this Table
		next_index = len(self.deck)
		card_x = self.pos[0]
		card_y = self.pos[1] + next_index * self.STACK_STRIDE

		# Set the position of the card
		card.set_dest((card_x, card_y))
		card.set_draggable()
		self.deck.append(card)

	def get_deck(self):
		return self.deck

	def update(self):
		for card in self.deck:
			card.update()

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
		self.shuffle()
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
			
	def shuffle(self):
		random.shuffle(self.deck)

class Trash(Deck):
	def __init__(self, pos):
		self.pos = pos
		self.deck = []
		self.base = Card(0, 0, self.pos)

	def place(self, card):
		card.set_dest(self.pos)
		self.deck.append(card)

	def render(self, screen):
		if self.is_empty():
			screen.blit(BJORUNDUR, self.pos)
		elif len(self.deck) == 1:
			screen.blit(BJORUNDUR, self.pos)
			self.top().render(screen)
		else:
			self.deck[-2].render(screen)
			self.top().render(screen)

class GameState:
	this_game = []
	def __init__(self):
		self.deck = Stack((40, 50))
		self.table = [Table((250 + 155*i, 50)) for i in range(NUM_DECKS)]
		self.trash = Trash((900, 460))

	def draw(self):
		if not self.deck.is_empty():
			hand = self.deck.draw()
			for i in range(NUM_DECKS):
				self.table[i].place(hand[i])

    # is_finished returns True if there are no legal moves to be made
    # in the current Game instance.
	def is_finished(self):
		finished = False
		if self.deck.is_empty():
			finished = True
			for i in range(0,NUM_DECKS):
				finished = finished and not self.can_discard(self.table[i].top(), i)
		return finished

    # can_discard checks whether *this* can be discarded
    # Takes a Card object and the index of the Table object
    # it came from.
	def can_discard(self, this, index):
		for i in range(0,NUM_DECKS):
			that = self.table[(index + i) % NUM_DECKS].top()
			if this.suit_buddies(that):
				if this < that:
					return True
		return False

	def auto_discard(self):
		#while True:
		#no_change = True
		for t in range(0, NUM_DECKS):
			if self.can_discard(self.table[t].top(), t):
				no_change = False
				card = self.table[t].pop()
				self.trash.place(card)
				self.log()
				break
		#if no_change:
		#	break

	def auto_move(self):
		for t in self.table:
			highest = None
			if t.is_empty():
				print("true")
				for a in self.table:
					if highest == None and a != None and not a.top().is_dummy():
						highest = a
					elif highest != None and highest.top() < a.top() and len(a.deck) > 1:
						highest = a
			if highest != None:
				t.place(highest.pop())
				self.log()

	# has_won checks whether the game has been won
	def has_won(self):
		victory = self.deck.is_empty()
		for i in range(0,NUM_DECKS):
			victory = victory and len(self.table[i].deck) == 1
		return victory	

	def dump_state(self):
		return { 'deck' : [card for card in self.deck.deck],
		'table' : [card for card in [table.deck for table in self.table]],
		'trash' : [card for card in self.trash.deck]
		 }

	def revert_to_state(self, state):
		self.deck.set_deck(state['deck'])
		for table in self.table:
			table.set_deck(state['table'])
		self.trash.set_deck(state['trash'])

	def log(self):
		self.this_game.append(self.dump_state())

class Game(GameState):
	# Game class inherits the GameState
	def __init__(self, screen):
		
		GameState.__init__(self)
		self.background_color = (80, 170, 80)
		self.screen = screen
		self.running = True
		self.current_card = None
		self.last_table = None
		self.BJORUNDUR = pygame.image.load('bjorundur.png')
		self.back_arrow = pygame.Surface((50, 50))
		self.back_arrow.fill((255, 0, 0))
	
	# Determine which table to drop to.
	def which_table(self, card):
		# Card can be dropped on many cards. Get largest intersection.
		collisions = []

		for table in self.table:
			top_card = table.top()
			# We detect the collision by finding which card is closest
			collisions.append(distSq(top_card.rect.center, card.rect.center))
		table = None
		dist_min = collisions[0]
		for i, collision in enumerate(collisions):
			if collision <= dist_min:
				dist_min = collision
				table = self.table[i]
		return table
		
	def end_game(self):
		self.running = False
		
	def handle_card_dropped(self, card):
		# TODO: Insert game logic, check if the move is legal
		table = self.which_table(card)
		# If card is dropped on any table, place card there
		if table:
			if table.is_empty():
				table.place(card)
				self.log()
				return True
		# Otherwise, return to original table
		return False

	# Check which card is pressed. Returns None if no card is pressed.
	def handle_back_arrow(self, mouse_pos):
		if self.back_arrow.get_rect().collidepoint(mouse_pos):
			print "handle"
			if len(self.this_game) > 1:
				popped = self.this_game.pop()
				print popped
				self.revert_to_state(self.this_game[-1])

	def handle_draw(self, mouse_pos):
		if not self.deck.is_empty():
			deck_rect = self.deck.get_rect()
			if deck_rect.collidepoint(mouse_pos):
				self.draw()
				self.log()

	def handle_trash(self, mouse_pos):
		if self.card_pressed(mouse_pos): 
			(card, table, index) = self.card_pressed(mouse_pos)
			if self.can_discard(card, index) and card.is_draggable():
				table.pop()
				self.trash.place(card)
				self.log()
	
	def card_pressed(self, mouse_pos):
		# Check if user wants to deal cards
		if not self.deck.is_empty():
			if self.deck.get_rect().collidepoint(mouse_pos):
				return None
		for table in self.table:
			for i, card in enumerate(table.get_deck()):
				if card.rect.collidepoint(mouse_pos) and card.is_draggable():
					return (card, table, i)

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
			
			if event.type == pygame.KEYDOWN:
				p = pygame.key.get_pressed()
				if p[pygame.K_d]:
					print("automate discard")
					self.auto_discard()
				if p[pygame.K_f]:
					print("automate move")
					self.auto_move()

			# Voluntary quit
			if event.type == pygame.QUIT:
				self.running = False	
	
			# Release the card if currently held, when releasing the mouse
			if event.type == pygame.MOUSEBUTTONUP:
				if self.current_card and self.last_table:
					if not self.handle_card_dropped(self.current_card):
						self.last_table.place(self.current_card)
					self.current_card.is_held = False
					self.current_card = None
					
			if event.type == pygame.MOUSEBUTTONDOWN:
				if not self.current_card:
					self.handle_back_arrow(mouse_pos)
					self.handle_trash(mouse_pos)
					self.handle_draw(mouse_pos)

			# If left mouse button is pressed, check if we're holding a card
			# if not, holding a card, set self.current_card to the card pressed
			if mouse_buttons == (1, 0, 0):
				if not self.current_card:
					if self.card_pressed(mouse_pos):
						(self.current_card, self.last_table, i) = self.card_pressed(mouse_pos)
						if self.current_card and self.last_table:
							self.current_card = self.last_table.top()
							self.current_card.is_held = True
							self.last_table.pop();
				else:
					self.current_card.nudge(mouse_delta)
	
		# If we're currently holding a card, update it
		for table in self.table:
			for card in table.deck:
				card.update()

		if self.trash.top():
			self.trash.top().update()

		if self.current_card:
			self.current_card.update()



	def render(self):
		# Render deck
		self.screen.fill(self.background_color)
		self.deck.render(self.screen)
		for table in self.table:
			table.render(self.screen)
		self.trash.render(self.screen)

		if self.current_card and not self.current_card.is_dummy():
			self.current_card.render(self.screen)

		# Render back arrow
		if len(self.this_game) > 1:
			self.screen.blit(self.back_arrow, (20, self.screen.get_rect().height-70))

		self.print_text(rules,30,260,16,25)
		
		if self.is_finished():
			self.print_text(defeat_status,400,300,20,25)
		
		if self.has_won():
			self.print_text(winning_status,400,300,20,25)
			
		# Update the screen.
		pygame.display.flip()

	def play(self):
		while self.running:
			self.update()
			self.render()

	def print_text(self,text,a,b,fontsize,diff):
		font_text = pygame.font.SysFont('assets/clarendon.ttf', fontsize)
		for line in text:
			self.screen.blit(font_text.render(line, True, (0,0,0)), (a, b))
			(a,b) = (a,b + diff) #Move each line 25 down
