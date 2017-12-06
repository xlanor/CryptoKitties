#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitties cmd.
# Written by xlanor
##

from tokens import Tokens
import datetime
import requests
import time
import json
from web3 import Web3, HTTPProvider, IPCProvider
import multiprocessing as mp
from multiprocessing import Pool
from telegram import ReplyKeyboardMarkup,ChatAction,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job,ConversationHandler
import traceback

class Commands():
	def broadcast(bot,update):
		return_array = []
		counter = 0
		trigger = True
		web3 = Web3(HTTPProvider('http://localhost:8545'))
		while trigger:
			try:
				url = "https://api.cryptokitties.co/auctions?offset="+str(counter)+"&limit=100&type=sale&status=open&sorting=cheap&orderBy=current_price&orderDirection=asc"
				sireurl = "https://api.cryptokitties.co/auctions?offset="+str(counter)+"&limit=100&type=sire&status=open&sorting=cheap&orderBy=current_price&orderDirection=asc"
				r = requests.get(url).json()
				q = requests.get(sireurl).json()
				if counter <= 1000:
					if r['auctions']:
						for kitten in r['auctions']:
							if kitten['kitty']['generation'] <= 6:
								if kitten['kitty']['status']['cooldown_index'] < 4:
									result = kitten['current_price']
									convertedeth = web3.fromWei(float(result),'ether')
									
									message = " Name: "
									message += str(kitten['kitty']['name']) if kitten['kitty']['name'] else "Null"
									message +="\nAddress: "
									message += str(kitten['kitty']['owner']['address']) if kitten['kitty']['owner']['address'] else "Null"
									message += "\nType: Sale "
									message += "\nGeneration: "
									message += str(kitten['kitty']['generation']) if kitten['kitty']['generation'] else "Null"
									message += "\nCooldown Index: "
									message += str(kitten['kitty']['status']['cooldown_index']) if kitten['kitty']['status']['cooldown_index'] else "Null"
									message += "\nETH: "
									message += str(convertedeth)
									bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
					if q['auctions']:
						for sirekitten in q['auctions']:
							if sirekitten['kitty']['generation'] <= 6:
								if sirekitten['kitty']['status']['cooldown_index'] < 4:
									result = sirekitten['current_price']

									convertedeth = web3.fromWei(float(result),'ether')
									
									message = " Name: "
									message += str(sirekitten['kitty']['name']) if sirekitten['kitty']['name'] else "Null"
									message +="\nAddress: "
									message += str(sirekitten['kitty']['owner']['address']) if sirekitten['kitty']['owner']['address'] else "Null"
									message += "\nType: Sire "
									message += "\nGeneration: "
									message += str(sirekitten['kitty']['generation']) if sirekitten['kitty']['generation'] else "Null"
									message += "\nCooldown Index: "
									message += str(sirekitten['kitty']['status']['cooldown_index']) if sirekitten['kitty']['status']['cooldown_index'] else "Null"
									message += "\nETH: "
									message += str(convertedeth)

									bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
					counter += 100
					print (str(counter)+" has been scraped")
				else:
					trigger = False
					current_time = datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")
					message = "API checked on "+current_time+"."
					bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
					
			except:
				#API will time out after x amount of requests. need to let it sleep then resume.
				catcherror = traceback.format_exc()
				bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=catcherror,parse_mode='HTML')

				message = """Timed out API on page number """+str(counter)+"""
							Sleeping for 15 seconds"""
				bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=message,parse_mode='HTML')
				time.sleep(15)