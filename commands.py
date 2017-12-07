#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitties cmd.
# Written by xlanor
##
from tokens import Tokens
import datetime
import time
import json
from telegram import ReplyKeyboardMarkup,ChatAction,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job,ConversationHandler
import traceback
from modules.broadcast import get_Data

class Commands():
	def broadcast(bot,update):
		try:
			data_dict = get_Data().thwinBC()
			if data_dict:
				for user,values in data_dict.items():
					for kid,kitten in values.items():
						message = " 🐈Name: "
						message += kitten["name"]
						message +="\n🏠Address: "
						message += kitten["address"]
						message += "\n📛ID: "
						message += kitten["id"]
						message += "\n🈹Type: Sale "
						message += "\n📈Generation: "
						message += kitten["gen"]
						message += "\n📈Cooldown Index: "
						message += kitten["cooldown"]
						message += "\n🚀ETH: "
						message += kitten["price"]
						message += "\n💻URL: "
						message += kitten["url"]
						message += "\nCattributes: "
						for index,tribute in enumerate(kitten["cattribute"]):
							message += tribute
							if index < (len(kitten["cattribute"])-1):
								message +=  ","

						if user == "thwin":
							message += "\n👨‍🚀Alerting: @nthwin @iczac @jaynertwx"
						else:
							message += "\n👨‍🚀Alerting: @kelvinleong"

						bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
		except:
			#All encompassing try excepts are generally not good idea.
			# but I want to be notified in this case.
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=catcherror,parse_mode='HTML')

