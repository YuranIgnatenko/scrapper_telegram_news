
from telethon import TelegramClient

import telethon
import models
import config
import logger
import os

session_file = "newSessionStatus"
config_file = 'config.json'
prefix = "app"
postfix = ".log"
name_bd_json = "test.json"
PATH_DIR_DOWNLOADS = "static/media_cache/"
EXTENSION_DOWNLOAD_FILE = ".jpg"


class ServiceTelegramScrapper:
	def __init__(self, config, logger):
		self.config  = config
		self.logger = logger
		self.scrapped_dialogs = []
		self.client = TelegramClient(
			session_file, 
			self.config["api_id"], 
			self.config["api_hash"])
		self.client.start()
		self.client.connect()
		
	def get_array_dialogs(self) -> list[telethon.types.Dialog]:
		temp_dialogs = []
		for dialog in self.client.iter_dialogs():
			if dialog.is_group or dialog.is_channel:
				temp_dialogs.append(dialog)
		return temp_dialogs

	def download_images_from_dialogs(self, array_dialogs:list[telethon.types.Dialog]) -> None:
		for dialog in array_dialogs:
			try:
				temp_namefile = self.client.download_media(dialog.message.photo)
				new_namefile = self.build_new_name_file(dialog.id)
				print(dir(temp_namefile), new_namefile)
				os.rename(temp_namefile, new_namefile)
			except Exception as e :
				print(e)
	
	def get_array_models_chats(self, array_dialogs:list[telethon.types.Dialog]) -> list[models.ModelLastDialog]:
		temp_array_chats = []
		for dialog in array_dialogs:
			temp_array_chats.append(
				models.ModelLastDialog(
					dialog.title,
					dialog.id, 
					dialog.message,
					dialog.date,
					dialog.name,
					self.build_new_name_file(dialog.id),
					self.build_new_name_file(dialog.id),
					))
		return temp_array_chats

	def build_new_name_file(self, dialog_id:int) -> str:
		return f"{PATH_DIR_DOWNLOADS}{dialog_id}{EXTENSION_DOWNLOAD_FILE}"


# conf = config.Config().to_dict()
# logger = logger.Logger(conf["log_file"])
# sts = ServiceTelegramScrapper(conf, logger)
# sts.get_array_models_chats(sts.get_array_dialogs())
# sts.download_images_from_dialogs(sts.get_array_dialogs())
