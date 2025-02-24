from telethon.sync import TelegramClient
import os, sys, json, time
import models
from PIL import Image
from io import BytesIO
import json, asyncio

session_file = "newSessionStatus"
config_file = 'config.json'
prefix = "app"
postfix = ".log"
name_bd_json = "test.json"


def save_to_json(array_objects, namefile):
	if os.path.isfile(namefile) == False:
		with open(namefile, "w")as file:file.close()
	list_json_obj = []
	for obj in array_objects:
		date_create = obj.date_create.replace(" ","-")
		data = {
			"id": obj.id,
			"name": obj.name,
			"message": obj.message,
			"date_create": date_create,	
			"image": obj.image,
		}
		list_json_obj.append(data)

	with open(namefile, 'a', encoding='utf-8') as file:
		json.dump(list_json_obj, file, ensure_ascii=False, indent=4)


class Config():
	def __init__(self):
		with open(config_file, 'r') as f:
			self.data = json.load(f)

class Logger():
	def __init__(self, filelog):
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


def update_data_json():
	conf = Config().data
	logger = Logger(conf["log_file"])

	client = TelegramClient(session_file, conf["api_id"], conf["api_hash"])
	client.connect()
	LIST_DIALOGS = []
	LIST_MODEL_LAST_DIALOGS = []

	for dialog in client.iter_dialogs():
		if dialog.is_group or dialog.is_channel:
			LIST_DIALOGS.append(dialog)

	for message in LIST_DIALOGS:
		try:
			s = client.download_media(message.message.photo)
			# not update file !!
			os.rename(s,f"static/media_cache/{message.id}.jpg")
		except Exception as e :
			continue

		LIST_MODEL_LAST_DIALOGS.append(
			models.ModelLastDialog(
				message.title,
				message.id, 
				message.message.message,
				message.message.date,
				message.name,
				f"static/media_cache/{message.id}.jpg",
				f"static/media_cache/{message.id}.jpg",
				))
		print("count", len(LIST_DIALOGS), len(LIST_MODEL_LAST_DIALOGS))

		try:
			img = message.message.photo.sizes[0].bytes
			LIST_MODEL_LAST_DIALOGS[-1].image_bytes = img
		except AttributeError as e:
			LIST_MODEL_LAST_DIALOGS[-1].image_bytes = "image_bytes_error_not_found"
	return LIST_MODEL_LAST_DIALOGS

if len(sys.argv)>1:
	mode = sys.argv[1]
	if mode == "1":
		save_to_json(update_data_json(), name_bd_json)