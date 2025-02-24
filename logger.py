
import os
import time

class Logger():
	def __init__(self, filelog:str):
		self.namefile = filelog
		self.check_file()
		self.add("created logger")

	def check_file(self):
		if os.path.isfile(self.namefile) == False:
			with open(self.namefile, "w+") as file:
				file.read() 
	
	def add(self, line):
		with open(self.namefile, "a") as file:
			file.write(f"{time.asctime()} [{line}]\n")
