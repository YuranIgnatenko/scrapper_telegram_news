import json
CONFIG_NAMEFILE = "config.json"

class Config():
	def __init__(self):
		with open(CONFIG_NAMEFILE, 'r') as f:
			self.data = json.load(f)

