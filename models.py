import json
from random import randint

class DataTemplateBlog():
	def __init__(self) -> None:
		self.head_text = "STN. Scrapper Telegram News"


class ModelDialog():
	def __init__(self, title, id, message, date_create, name, image, image_bytes) -> None:
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

class PageModelDialog():
	def __init__(self,namefile_json:str, max_items_in_page:int) -> None:
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
		self.max_items_in_page = max_items_in_page
		self.now_index_page = 0

	def get_list_items_dialog(self) -> list[ModelDialog]:
		try:
			return self.lmld[self.now_index_page*self.max_items_in_page:self.now_index_page*self.max_items_in_page+self.max_items_in_page]
		except Exception as e:
			return self.lmld

	def get_item_dialog(self, id:int) -> ModelDialog:
		for elem in self.lmld:
			if str(elem['id']) == str(id):
				return elem
			
	def get_list_items_dialog_random(self, count:int) -> list[ModelDialog]:
		temp_collect = []
		for i in range(count):
			temp_collect.append(self.lmld[randint(0,len(self.lmld)-1)])
		return temp_collect
