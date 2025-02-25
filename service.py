from telethon.sync import TelegramClient
import telethon
import os, sys
import models

import json

import config
import logger

class ServiceScrapperDialogs():
	def __init__(self, conf:config.Config, log:logger.Logger) -> None:
		self.conf = conf
		self.log = log
		self.namefile_bd = self.conf.get("bd_file")
		self.path_image_cache = self.conf.get("path_image_cache")
		self.ext_image_file = self.conf.get("ext_image_file")

	def save_to_json(self, array_dialogs:list[telethon.types.Dialog]) -> None:
		self.ping_file_bd()

		temp_array_dialogs_json = []	
		
		for dialog in array_dialogs:
			temp_dict_json_element = self.new_dict_json_element(dialog)
			temp_array_dialogs_json.append(temp_dict_json_element)

		with open(self.namefile_bd, 'w', encoding='utf-8') as file:
			json.dump(temp_array_dialogs_json, file, ensure_ascii=False, indent=4)

	def new_dict_json_element(self, dialog:telethon.types.Dialog) -> dict:
		temp_date_create = dialog.date_create.replace(" ","-")
		temp_dict_json_element = {
			"id": dialog.id,
			"name": dialog.name,
			"message": dialog.message,
			"date_create": temp_date_create,	
			"image": dialog.image,
		}
		return temp_dict_json_element

	def ping_file_bd(self) -> None:
		if self.is_exists_file() == False:
			with open(self.namefile_bd, "w") as bd:
				bd.close()

	def is_exists_file(self) -> bool:
		return os.path.isfile(self.namefile_bd)

	def create_telegram_client(self) -> None:
		self.client = TelegramClient(
			self.conf.get("session_file"), 
			self.conf.get("api_id"), 
			self.conf.get("api_hash"))
		self.client.connect()

	def update_data_json(self) -> None:
		self.create_telegram_client()

		array_channel_dialogs = []
		array_model_dialogs = []

		for dialog in self.client.iter_dialogs():
			if dialog.is_group or dialog.is_channel:
				array_channel_dialogs.append(dialog)

		self.remove_cache_image()

		for dialog in array_channel_dialogs:
			self.try_download_image(dialog)

			array_model_dialogs.append(
				models.ModelLastDialog(
					dialog.title,
					dialog.id, 
					dialog.message.message,
					dialog.message.date,
					dialog.name,
					self.build_new_name_image(id),
					self.build_new_name_image(id),
					))
			print("count", len(array_channel_dialogs), len(array_model_dialogs))

		return array_model_dialogs

	def try_download_image(self, dialog:telethon.types.Dialog) -> None:
			temp_name_image = self.save_image(dialog)
			if temp_name_image is None: return
			self.rename_image(temp_name_image, dialog.id)

	def save_image(self, dialog:telethon.types.Dialog) -> str:
		try:temp_name_image = self.client.download_media(dialog.message.photo)
		except Exception as e: print(e)
		return temp_name_image

	def rename_image(self, name_image:str, id:int) -> None:
		try:os.rename(name_image, self.build_new_name_image(id))
		except Exception as e: print(e)

	def remove_cache_image(self) -> None:
		try:os.remove(self.path_image_cache)
		except Exception as e: print(e)
		try:os.makedirs(self.path_image_cache)
		except Exception as e: print(e)

	def build_new_name_image(self, id:int) -> str:
		return f"{self.path_image_cache}{id}{self.ext_image_file}"

def main():
	if len(sys.argv)>1:
		arg_namefile_config = sys.argv[1]
		conf = config.Config(sys.argv[1])
		log = logger.Logger(conf.get("log_file"))
		ssd = ServiceScrapperDialogs(conf, log)
		ssd.update_data_json()
	else:
		print("enter setup-params for file")
		return

if __name__ == "__main__":
	main()