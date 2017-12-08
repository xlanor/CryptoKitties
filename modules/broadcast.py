#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Broadcast Module
# Written by xlanor
##
import json,traceback,requests,sys,wand,os,contextlib
from web3 import Web3, HTTPProvider, IPCProvider
import time
from wand.image import Image
sys.path.append("/home/elanor/ftp/files/cryptokitties")

sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries = 20)
sess.mount('https://', adapter)

class get_Data():
	def cat_list(self):
		# list of some rare cattributes
		cat_list = ["calicool","tigerpunk","spock","beard","mauveover","cymric","gold","otaku","saycheese","googly","mainecoon","whixtensions","wingtips","chestnut","jaguar"]
		return cat_list

	def urls(self,user):
		user_gen = self.generation(user)
		user_list = list(range(0,user_gen+1))
		url = "&limit=100&type=sale&status=open&sorting=cheap&orderBy=current_price&orderDirection=asc&"
		for index,number in enumerate(user_list):
			url += "gen:"
			url += str(number)
			if (index < (len(user_list) -1)):
				url += "+"
		return url

	def generation(self,user): #generation index to search for.
		if user == "thwin":
			return 5
		else:
			return 2

	def cooldown (self,user): #cooldown index to search for.
		if user == "thwin":
			return 4
		else:
			return 1

	def colleagues(self): # my colleagues, different values based on what they want
		return ["thwin","kelvin"]

	def offset(self,user): #offset values min and max. Not reccomended to scan until infinity.
		if user == "thwin":
			return [0,2000]
		else:
			return [8188,11000]
	def image_filepath(self):
		#modify this to where you want cat pictures to be saved
		return "/home/elanor/ftp/files/cryptokitties/modules/kitty_pictures/"




	def thwinBC(self):
		return_dict = {}
		web3 = Web3(HTTPProvider('http://localhost:8545'))
		colleague_counter = 0
		while (colleague_counter < len(self.colleagues())):
			
			trigger = True
			user = self.colleagues()[colleague_counter]
			counter = self.offset(user)[0]
			while trigger:
				try:
					# Pull the auction api data,
					url = "https://api.cryptokitties.co/auctions?offset="+str(counter)+self.urls(user)
					json_data = sess.get(url).json()
					if counter <= self.offset(user)[1]:
						if json_data['auctions']:
							# for each cat,
							for kitten in json_data['auctions']:
								found_cat_trigger = False
								#set the found cat to false first, then check generation and cooldown.
								if kitten['kitty']['generation'] <= self.generation(user) and kitten['kitty']['status']['cooldown_index'] < self.cooldown(user):
									#We found a cat! lets check cattributes
									cattribute_api = "https://api.cryptokitties.co/kitties/"+str(kitten['kitty']['id'])
									cattribute = sess.get(cattribute_api).json()
									cat_image_url = cattribute['image_url']
									cattribute_list = cattribute['cattributes']

									cattribute_list = [x["description"] for x in cattribute_list]
									for index,val in enumerate(cattribute_list):	
										if val in self.cat_list():
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
										if user in return_dict:
											return_dict[user][str(kitten['kitty']['id'])]=found_cat
										else:
											return_dict[user] = {}
											return_dict[user][str(kitten['kitty']['id'])]=found_cat

							print(str(counter) + " scraped")
							counter += 100
						else:
							#if not r auctions means the api timed.
							time.sleep(15)
					else:
						trigger = False
						colleague_counter += 1
				except Exception as e:
					if "Invalid Retry-After header:" not in str(e): #only log exceptions that arent invalid retries.
						with open('logs.txt','a') as f:
							f.write(str(e))
							f.write(traceback.format_exc())
		return return_dict

#debugging stuff, prints the output as a standalone mod for me to see.
if __name__ == '__main__':
	print(get_Data().thwinBC())
