from telethon.sync import TelegramClient
import telethon
import os, sys
import models

import json

import config
import logger
import bd

import shutil


class ServiceScrapperDialogs():
	def __init__(self, conf:config.Config, log:logger.Logger, bd:bd.ControlBD) -> None:
		self.conf = conf
		self.log = log
		self.ctrlbd = bd
		self.namefile_bd = self.conf.get("bd_file")
		self.path_image_cache = self.conf.get("path_image_cache")
		self.ext_image_file = self.conf.get("ext_image_file")
		self.limit_scrap_dialogs = int(self.conf.get("limit_scrap_dialogs"))

	def save_in_bd(self, array_dialogs:list[telethon.types.Dialog]) -> None:
		self.ctrlbd.ping_connection_bd()

		temp_array_dialogs_json = []	
		
		for dialog in array_dialogs:
			temp_dict_json_element = self.dialog_to_json_dict(dialog)
			temp_array_dialogs_json.append(temp_dict_json_element)

		self.ctrlbd.json_dump_array_dialogs(temp_array_dialogs_json)


	def dialog_to_json_dict(self, dialog:telethon.types.Dialog) -> dict:
		temp_date_create = dialog.date_create.replace(" ","-")
		temp_dict_json_element = {
			"id": dialog.id,
			"name": dialog.name,
			"message": dialog.message,
			"date_create": temp_date_create,	
			"image": dialog.image,
		}
		return temp_dict_json_element

	def create_telegram_client(self) -> None:
		self.client = TelegramClient(
			self.conf.get("session_file"), 
			self.conf.get("api_id"), 
			self.conf.get("api_hash"))
		self.client.connect()

	def get_array_channel_dialogs(self) -> list[telethon.types.Dialog]:
		temp_array_model_dialogs = []

		for dialog in self.client.iter_dialogs(limit=self.limit_scrap_dialogs):
			if dialog.is_group or dialog.is_channel:
				temp_array_model_dialogs.append(dialog)

		return temp_array_model_dialogs

	def launch(self) -> None:
		self.ctrlbd.remove_cache_image()

		array_model_dialogs = []
		array_channel_dialogs =  self.get_array_channel_dialogs()

		for dialog in array_channel_dialogs:
			temp_name_image = self.try_download_image(dialog)
			array_model_dialogs.append(self.create_model_dialog(dialog, temp_name_image))
			print("count", len(array_model_dialogs), len(array_channel_dialogs))

		self.save_in_bd(array_model_dialogs)
		
	def create_model_dialog(self, dialog:telethon.types.Dialog, image_name:str) -> models.ModelDialog:
		temp_dialog = models.ModelDialog(
			dialog.title,
			dialog.id, 
			dialog.message.message,
			dialog.message.date,
			dialog.name,
			image_name,
			image_name,
			)
		return temp_dialog

	def try_download_image(self, dialog:telethon.types.Dialog) -> str:
			temp_name_image = self.save_image(dialog)
			if temp_name_image is None: 
				temp_name_image = self.conf.get("news_default_image")
				shutil.copy(temp_name_image, self.build_new_name_image(dialog.id))
				return self.build_new_name_image(dialog.id)
			self.ctrlbd.rename_image(temp_name_image, self.build_new_name_image(dialog.id))
			return temp_name_image

	def save_image(self, dialog:telethon.types.Dialog) -> str:
		try:
			temp_name_image = self.client.download_media(
				dialog.message.photo, f"{self.path_image_cache}{dialog.id}{self.ext_image_file}")
			return temp_name_image
		except Exception as e: 
			temp_name_image = self.conf.get("news_default_image")
		return temp_name_image

	def build_new_name_image(self, id:int) -> str:
		return f"{self.path_image_cache}{id}{self.ext_image_file}"

def main():
	if len(sys.argv)>1:
		arg_namefile_config = sys.argv[1]

		conf = config.Config(arg_namefile_config)
		log = logger.Logger(conf)
		ctrlbd = bd.ControlBD(conf)
		ssd = ServiceScrapperDialogs(conf, log, ctrlbd)

		ssd.create_telegram_client()
		ssd.launch()
	else:
		print("enter setup-params for file")
		return

if __name__ == "__main__":
	main()