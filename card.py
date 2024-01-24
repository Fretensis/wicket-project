class Card:
	coins = 0
	block = False
	date = 5
	name = ''

	def __init__(self, coins, block, date, name):
		self.coins = coins
		self.block = block
		self.date = date
		self.name = name
