class card:
	def __init__(suit, rank):
		self.suit = suit
		self.rank = rank

	def draw_at(self, at):
		# Gets suit image
		# Assembles card image
		# Blits to pygame screen at location