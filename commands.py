#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitties cmd.
# Written by xlanor
##
from ghost import Ghost
import urllib.request
from tokens import Tokens
import datetime
import requests
import time
import json
import os
from web3 import Web3, HTTPProvider, IPCProvider
import multiprocessing as mp
from multiprocessing import Pool
from telegram import ReplyKeyboardMarkup,ChatAction,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job,ConversationHandler
import traceback
import contextlib

class Commands():
	def broadcast(bot,update):
		ghost = Ghost()
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
							if kitten['kitty']['generation'] <= 7:
								if kitten['kitty']['status']['cooldown_index'] < 4:
									cattribute_api = "https://api.cryptokitties.co/kitties/"+str(kitten['kitty']['id'])
									cattribute = requests.get(cattribute_api).json()
									cattribute_list = cattribute['cattributes']
									for each in cattribute_list:
										if each in cat_list:
											result = kitten['current_price']
											convertedeth = web3.fromWei(float(result),'ether')
											message = " 🐈Name: "
											message += str(kitten['kitty']['name']) if kitten['kitty']['name'] else "Null"
											message +="\n🏠Address: "
											message += str(kitten['kitty']['owner']['address']) if kitten['kitty']['owner']['address'] else "Null"
											message += "\n📛ID: "
											message += str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
											message += "\n🈹Type: Sale "
											message += "\n📈Generation: "
											message += str(kitten['kitty']['generation']) if kitten['kitty']['generation'] else "Null"
											message += "\n📈Cooldown Index: "
											message += str(kitten['kitty']['status']['cooldown_index']) if kitten['kitty']['status']['cooldown_index'] else "Null"
											message += "\n🚀ETH: "
											message += str(convertedeth)
											message += "\n💻URL: "
											message += "https://www.cryptokitties.co/kitty/"
											message += str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
											message += "\nCattributes: "
											for x in cattribute_list:
												if x in cat_list:
													message += "<b>"
													message += str(x)
													message += "</b>"
												else:
													message += str(x)
												message += ", "
											message += "\n👨‍🚀Alerting: @nthwin @iczac @jaynertwx"
											filename = "/home/elanor/ftp/files/cryptokitties/images/"+str(kitten['kitty']['id'])+".png"
											with ghost.start() as session:
												session.open(cattribute['image_url'])
												session.capture_to(filename)
											"""
											svg_filename  = "/home/elanor/ftp/files/cryptokitties/images/"+str(kitten['kitty']['id'])+".svg"
											
											f = open(svg_filename,'wb')
											f.write(urllib.request.urlopen(cattribute['image_url']).read())
											f.close()
											cairosvg.svg2png(url=svg_filename, write_to=filename)"""

											bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
											bot.sendPhoto(chat_id=Tokens.channel('livechannel'),photo=open(filename,'rb'))
											os.remove(filename)
											break

					scrapednumber = "Nthwin "+str(counter)+" scraped"
					counter += 100
					bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=scrapednumber,parse_mode='HTML')
					print (str(counter)+" has been scraped")
				else:
					trigger = False
					
			except:
				#API will time out after x amount of requests. need to let it sleep then resume.
				catcherror = traceback.format_exc()
				bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=catcherror,parse_mode='HTML')

				message = """Timed out API on page number """+str(counter)+"""
							Sleeping for 15 seconds"""
				bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=message,parse_mode='HTML')
				time.sleep(15)

	def kleongbroadcast(bot,update):
		ghost = Ghost()
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
											message = "🐈 Name: "
											message += str(kitten['kitty']['name']) if kitten['kitty']['name'] else "Null"
											message +="\n🏠Address: "
											message += str(kitten['kitty']['owner']['address']) if kitten['kitty']['owner']['address'] else "Null"
											message += "\n📛ID: "
											message += str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
											message += "\n🈹Type: Sale "
											message += "\n📈Generation: "
											message += str(kitten['kitty']['generation']) if kitten['kitty']['generation'] else "Null"
											message += "\n📈Cooldown Index: "
											message += str(kitten['kitty']['status']['cooldown_index']) if kitten['kitty']['status']['cooldown_index'] else "Null"
											message += "\n🚀ETH: "
											message += str(convertedeth)
											message += "\n💻URL: "
											message += "https://www.cryptokitties.co/kitty/"
											message += str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
											message += "\nCattributes: "
											for x in cattribute_list:
												if x in cat_list:
													message += "<b>"
													message += str(x)
													message += "</b>"
												else:
													message += str(x)
												message += ", "
											message += "\n👨‍🚀Alerting: @kelvinleong"
											filename = "/home/elanor/ftp/files/cryptokitties/images/"+str(kitten['kitty']['id'])+".png"
											with ghost.start() as session:
												session.open(cattribute['image_url'])
												session.capture_to(filename)
											bot.sendMessage(chat_id=Tokens.channel('livechannel'),text=message,parse_mode='HTML')
											bot.sendPhoto(chat_id=Tokens.channel('livechannel'),photo=cattribute['image_url'])
											bot.sendPhoto(chat_id=Tokens.channel('livechannel'),photo=open(filename,'rb'))
											os.remove(filename)
											break
					counter += 100
					print ("Kleong"+ str(counter)+" has been scraped")
				else:
					kleongTrigger = False	
					
			except:
				#API will time out after x amount of requests. need to let it sleep then resume.
				catcherror = traceback.format_exc()
				bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=catcherror,parse_mode='HTML')

				message = """Timed out Kleong API on page number """+str(counter)+"""
							Sleeping for 15 seconds"""
				bot.sendMessage(chat_id=Tokens.channel('errorchannel'),text=message,parse_mode='HTML')
				time.sleep(15)