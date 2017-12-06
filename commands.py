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
				if counter <= 100:
					if r['auctions']:
						for kitten in r['auctions']:
							if kitten['kitty']['generation'] <= 6:
								if kitten['kitty']['status']['cooldown_index'] < 4:
									result = kitten['current_price']
									convertedeth = web3.fromWei(float(result),'ether')
									message = """Name: """+kitten['kitty']['name']+"""\n
												Address: """+kitten['kitty']['owner']['address']+"""\n
												Type: Sale
												Generation: """+kitten['kitty']['status']['cooldown_index']+"""
												Cooldown Index: """+kitten['kitty']['status']['cooldown_index']+"""
												ETH: """+str(convertedeth)

									bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
					if q['auctions']:
						for sirekitten in q['auctions']:
							if sirekitten['kitty']['generation'] <= 6:
								if sirekitten['kitty']['status']['cooldown_index'] < 4:
									result = sirekitten['current_price']
									convertedeth = web3.fromWei(float(result),'ether')
									message = """Name: """+sirekitten['kitty']['name']+"""\n
												Address: """+sirekitten['kitty']['owner']['address']+"""\n
												Type: Sire
												Generation: """+kitten['kitty']['status']['cooldown_index']+"""
												Cooldown Index: """+kitten['kitty']['status']['cooldown_index']+"""
												ETH: """+str(convertedeth)

									bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
					counter += 1
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