import os
import time

class Logger():
	def __init__(self, namefile:str) -> None:
		self.namefile = namefile
		self.connect_file()

	def is_exists_file(self) -> bool:
		return os.path.isfile(self.namefile)

	def connect_file(self) -> None:
		if self.is_exists_file == False:
			with open(self.namefile, "w+") as file:
				file.read() 
	
	def add(self, line:any) -> None:
		with open(self.namefile, "a") as file:
			file.write(f"{time.asctime()} [{line}]\n")
