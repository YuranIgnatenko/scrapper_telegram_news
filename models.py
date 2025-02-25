import json
from random import randint

class DataTemplateBlog():
	def __init__(self) -> None:
		self.head_text = "STN. Scrapper Telegram News"


class ModelLastDialog():
	def __init__(self, title, id, message, date_create, name, image, image_bytes):
		self.title = title
		self.message = message
		self.preview_text = 0
		self.id = id
		self.date_create = f"{date_create}"
		self.name = name
		self.image = image
		self.image_bytes = image_bytes
		self.view = 0
		self.forward = 0
		self.source = 0

class PageModelLastDialog():
	def __init__(self,namefile_json):
		with open(namefile_json, 'r', encoding='utf-8') as file:
			json_data = file.read()
		self.data = json.loads(json_data)
		for dt in self.data:
			try:
				dt['desc'] = dt["message"][:30]
			except Exception as e :
				dt['desc'] = "Description not found"
				continue
		list_model_last_dialog = self.data
		self.lmld = list_model_last_dialog
		self.max_in_page = 4
		self.now_page = 0
	def get_page(self):
		try:
			return self.lmld[self.now_page*self.max_in_page:self.now_page*self.max_in_page+self.max_in_page]
		except Exception as e:
			return self.lmld
	def get_obj_from_id(self, id):
		for elem in self.lmld:
			if str(elem['id']) == str(id):
				return elem
			
	def get_random_collect(self, count=4):
		temp_collect = []
		for i in range(count):
			temp_collect.append(self.lmld[randint(0,len(self.lmld)-1)])
		return temp_collect
			

class ModelSingle():
	def __init__(self,data):
		self.data = data