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
		cat_list = ["spock","beard","mauveover","cymric","gold","otaku","saycheese","googly","mainecoon","whixtensions","wingtips","chestnut","jaguar"]
		counter = 0
		trigger = True
		web3 = Web3(HTTPProvider('http://localhost:8545'))
		while trigger:
			try:
				url = "https://api.cryptokitties.co/auctions?offset="+str(counter)+"&limit=100&type=sale&status=open&sorting=cheap&orderBy=current_price&orderDirection=asc"
				#sireurl = "https://api.cryptokitties.co/auctions?offset="+str(counter)+"&limit=100&type=sire&status=open&sorting=cheap&orderBy=current_price&orderDirection=asc"
				r = requests.get(url).json()
				#q = requests.get(sireurl).json()
				if counter <= 1000:
					if r['auctions']:
						for kitten in r['auctions']:
							if kitten['kitty']['generation'] <= 6:
								if kitten['kitty']['status']['cooldown_index'] < 4:
									cattribute_api = "https://api.cryptokitties.co/kitties/"+str(kitten['kitty']['id'])
									cattribute = requests.get(cattribute_api).json()
									cattribute_list = cattribute['cattributes']
									for each in cattribute_list:
										if each in cat_list:
											result = kitten['current_price']
											convertedeth = web3.fromWei(float(result),'ether')
											message = " Name: "
											message += str(kitten['kitty']['name']) if kitten['kitty']['name'] else "Null"
											message +="\nAddress: "
											message += str(kitten['kitty']['owner']['address']) if kitten['kitty']['owner']['address'] else "Null"
											message += "\n ID: "
											message += str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
											message += "\nType: Sale "
											message += "\nGeneration: "
											message += str(kitten['kitty']['generation']) if kitten['kitty']['generation'] else "Null"
											message += "\nCooldown Index: "
											message += str(kitten['kitty']['status']['cooldown_index']) if kitten['kitty']['status']['cooldown_index'] else "Null"
											message += "\nETH: "
											message += str(convertedeth)
											message += "\nURL: "
											message += "https://www.cryptokitties.co/kitty/"
											message += str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
											message += "\nCattributes: "
											for x in cattribute_list:
												message += str(x)
												message += ","
											message += "\n@nthwin @iczac"

											bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
											break

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

	def kleongbroadcast(bot,update):
		cat_list = ["spock","beard","mauveover","cymric","gold","otaku","saycheese","googly","mainecoon","whixtensions","wingtips","chestnut","jaguar"]
		counter = 7188
		kleongTrigger = True
		web3 = Web3(HTTPProvider('http://localhost:8545'))
		while kleongTrigger:
			try:
				kleong_url1 = "https://api.cryptokitties.co/auctions?offset="+str(counter)+"&limit=100&type=sale&status=open&sorting=cheap&orderBy=current_price&orderDirection=asc"
				r = requests.get(kleong_url1).json()
				#q = requests.get(sireurl).json()
				if counter <= 8388:
					if r['auctions']:
						for kitten in r['auctions']:
							if kitten['kitty']['generation'] <= 2:
								if kitten['kitty']['status']['cooldown_index'] <= 1:
									cattribute_api = "https://api.cryptokitties.co/kitties/"+str(kitten['kitty']['id'])
									cattribute = requests.get(cattribute_api).json()
									cattribute_list = cattribute['cattributes']
									result = kitten['current_price']
									for each in cattribute_list:
										if each in cat_list:
											convertedeth = web3.fromWei(float(result),'ether')
											message = " Name: "
											message += str(kitten['kitty']['name']) if kitten['kitty']['name'] else "Null"
											message +="\nAddress: "
											message += str(kitten['kitty']['owner']['address']) if kitten['kitty']['owner']['address'] else "Null"
											message += "\n ID: "
											message += str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
											message += "\nType: Sale "
											message += "\nGeneration: "
											message += str(kitten['kitty']['generation']) if kitten['kitty']['generation'] else "Null"
											message += "\nCooldown Index: "
											message += str(kitten['kitty']['status']['cooldown_index']) if kitten['kitty']['status']['cooldown_index'] else "Null"
											message += "\nETH: "
											message += str(convertedeth)
											message += "\nURL: "
											message += "https://www.cryptokitties.co/kitty/"
											message += str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
											message += "\nCattributes: "
											for x in cattribute_list:
												message += str(x)
												message += ","
											message += "\n@kelvinleong"

											bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
					counter += 100
					print ("Kleong"+ str(counter)+" has been scraped")
				else:
					kleongTrigger = False
					current_time = datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")
					message = "Kleong API checked on "+current_time+"."
					bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
					
			except:
				#API will time out after x amount of requests. need to let it sleep then resume.
				catcherror = traceback.format_exc()
				bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=catcherror,parse_mode='HTML')

				message = """Timed out Kleong API on page number """+str(counter)+"""
							Sleeping for 15 seconds"""
				bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=message,parse_mode='HTML')
				time.sleep(15)