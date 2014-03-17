class card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __repr__(self):
		return "[ " + self.suit + " " + str(self.rank) + " ]"

	def draw_at(self, at):
		# Gets suit image
		# Assembles card image
		# Blits to pygame screen at location
		