#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Broadcast User Module
# Written by xlanor
##

import json,traceback,requests,sys,wand,os,contextlib,pymysql
from contextlib import closing
from web3 import Web3, HTTPProvider, IPCProvider
import time
from wand.image import Image



sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries = 20)
sess.mount('https://', adapter)

class get_Data_Individual():
	def urls(self,user_gen):
		user_list = list(range(0,user_gen+1))
		url = "&limit=100&type=sale&status=open&sorting=cheap&orderBy=current_price&orderDirection=asc&search="
		for index,number in enumerate(user_list):
			url += "gen:"
			url += str(number)
			if (index < (len(user_list) -1)):
				url += "+"
		return url

	def image_filepath(self):
		#modify this to where you want cat pictures to be saved
		picturedir = os.path.join(os.path.dirname(__file__), 'kitty_pictures/')
		return picturedir


	def broadcast_user(self,user_info,att_list):
		return_dict = {}
		web3 = Web3(HTTPProvider('http://localhost:8545'))
		trigger = True
		counter = user_info[3]
		while trigger:
			try:
				url = "https://api.cryptokitties.co/auctions?offset="+str(counter)+self.urls(user_info[1])
				json_data = sess.get(url).json()
				if counter <= user_info[4]:
					if json_data['auctions']:
						# for each cat,
						for kitten in json_data['auctions']:
							found_cat_trigger = False
							# No need to check generation, because we have restricte dit in the api url.
							if  kitten['kitty']['status']['cooldown_index'] < user_info[2]:
								cattribute_api = "https://api.cryptokitties.co/kitties/"+str(kitten['kitty']['id'])
								cattribute = sess.get(cattribute_api).json()
								cat_image_url = cattribute['image_url']
								cattribute_list = cattribute['cattributes']
								cattribute_list = [x["description"] for x in cattribute_list]
								for index,val in enumerate(cattribute_list):
									if val in att_list:
										#formats it for tg output if found, change bool var to true.
										cattribute_list[index] = "".join(['<b>',val,"</b>"])
										found_cat_trigger = True
								if found_cat_trigger:
									found_cat = {}
									#pull data out
									current_price = kitten['current_price']
									convertedeth = web3.fromWei(float(current_price),'ether')
									found_cat["name"] = str(kitten['kitty']['name']) if kitten['kitty']['name'] else "Null"
									found_cat["address"] = str(kitten['kitty']['owner']['address']) if kitten['kitty']['owner']['address'] else "Null"
									found_cat["id"] = str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"
									found_cat["gen"] =  str(kitten['kitty']['generation']) if kitten['kitty']['generation'] else "Null"
									found_cat["cooldown"] = str(kitten['kitty']['status']['cooldown_index']) if kitten['kitty']['status']['cooldown_index'] else "Null"
									found_cat["price"] = str(convertedeth)
									found_cat["url"] = ("https://www.cryptokitties.co/kitty/" + (str(kitten['kitty']['id']) if kitten['kitty']['id'] else "Null"))
									found_cat["cattribute"] = cattribute_list
									#save image file and place the file path in the array so that we can access it later
									image_response = sess.get(cat_image_url)
									if image_response.status_code == 200:
										filepath = "".join([self.image_filepath(),str(kitten['kitty']['id']),".svg"])
										jpgfilepath = "".join([self.image_filepath(),str(kitten['kitty']['id']),".jpg"])
										with open(filepath,"wb") as f:
											f.write(image_response.content)
										with Image(filename=filepath) as img:
											img.format = 'jpg'
											img.save(filename=jpgfilepath)
											os.remove(filepath) #deletes vector file
											found_cat["image"] = jpgfilepath
									# put into a dictionary to return.
									if str(kitten['kitty']['id']) not in return_dict:
										return_dict[str(kitten['kitty']['id'])] = {}
										return_dict[str(kitten['kitty']['id'])]=found_cat

						print(str(counter) + " scraped")
						counter += 100
					else:
						#if not r auctions means the api timed.
						time.sleep(15)	
				else:
					trigger = False			
			except Exception as e:
				if "Invalid Retry-After header:" not in str(e): #only log exceptions that arent invalid retries.
					with open('logs.txt','a') as f:
						f.write(str(e))
						f.write(traceback.format_exc())
		return return_dict