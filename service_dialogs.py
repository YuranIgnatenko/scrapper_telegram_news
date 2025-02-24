from telethon.sync import TelegramClient
import os, sys, json, time
import models
from PIL import Image
from io import BytesIO
import json, asyncio




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


if len(sys.argv)>1:
	mode = sys.argv[1]
	if mode == "1":
		save_to_json(update_data_json(), name_bd_json)