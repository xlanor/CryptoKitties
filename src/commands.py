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
import ssl
import os
import pymysql
from telegram import ReplyKeyboardMarkup,ChatAction,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job,ConversationHandler
import traceback
from modules.broadcast_users import get_Data_Individual
from contextlib import closing

GENERATION,COOLDOWN,OFFSTART,OFFEND,ATTLIST = range(5)

class Commands():
	def __init__(self):
		token_list = Tokens().mysql()
		self.conn = pymysql.connect(**token_list)
		self.conn.autocommit(True)


	def register(self, bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				cur.execute("""SELECT telegram_id FROM User WHERE telegram_id = %s""",(uid,))
				if cur.rowcount == 0:
					message = "Registering you in my database! \n"
					message += "Can I please have the generation index?\n"
					message += "This bot will search for the generation index less than or equals to the number you input\n"
					message += "If you feel threatened at any point of time, do a /cancel to abort this conversation."
					cur.execute("""INSERT INTO User VALUES(%s,NULL,NULL,NULL,NULL,'No')""",(uid,))
					update.message.reply_text(message,parse_mode='HTML')
					return GENERATION
				else:
					message = "You are already registered in my database. To remove your details, do a /forget"
					update.message.reply_text(message,parse_mode='HTML')
					return ConversationHandler.END


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def generation(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				try:
					int(update.message.text)
				except ValueError:
					message = "Please send me an integer :)"
					update.message.reply_text(message,parse_mode='HTML')
					return GENERATION
				else:
					cur.execute("""UPDATE User SET generation_index = %s WHERE telegram_id =  %s""",(update.message.text,uid,))
					message = "Fantastic. Now, may I please have a cooldown index?"
					message += "This bot will scan for the cooldown index less than the number that you input"
					update.message.reply_text(message,parse_mode='HTML')
					return COOLDOWN


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def cooldown(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				try:
					int(update.message.text)
				except ValueError:
					message = "Please send me an integer :)"
					update.message.reply_text(message,parse_mode='HTML')
					return COOLDOWN
				else:
					cur.execute("""UPDATE User SET cooldown_index = %s WHERE telegram_id =  %s""",(update.message.text,uid,))
					message = "Fantastic. Now, may I please have the offset starting point?"
					message += "This bot will scan the api starting at the offset given. We recomend starting at 0"
					update.message.reply_text(message,parse_mode='HTML')
					return OFFSTART


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def offstart(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				try:
					int(update.message.text)
				except ValueError:
					message = "Please send me an integer :)"
					update.message.reply_text(message,parse_mode='HTML')
					return OFFSTART
				else:
					cur.execute("""UPDATE User SET offset_start = %s WHERE telegram_id =  %s""",(update.message.text,uid,))
					message = "Fantastic. Now, may I please have the offset end point?"
					message += "This bot will scan the api starting from the offset start to the offset end. It's not recomended to have a large range.\n"
					message += "A range of about 200 is recomended."
					update.message.reply_text(message,parse_mode='HTML')
					return OFFEND



		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def offend(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				try:
					int(update.message.text)
				except ValueError:
					message = "Please send me an integer :)"
					update.message.reply_text(message,parse_mode='HTML')
					return OFFEND
				else:
					cur.execute("""UPDATE User SET offset_end = %s WHERE telegram_id =  %s""",(update.message.text,uid,))
					message = "Thank you, now, please key in a cattribute(one cattribute at a time only!)"
					message += "This bot will match the cattributes you are looking for"
					update.message.reply_text(message,parse_mode='HTML')
					return ATTLIST

		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def attribute_list(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				if str.lower(update.message.text) == "end":
					message = "Thanks for registering =)\n"
					message = "If you want to toggle 10 minute scans, please do a /alert"
					update.message.reply_text(message,parse_mode='HTML')
					return ConversationHandler.END
				else:
					cur.execute("""INSERT INTO Attribute VALUES(%s,%s)""",(uid,update.message.text,))
					message= update.message.text
					message += " has been added as an attribute. Please enter the next attribute \n"
					message += "If you're done with adding your cattributes, please reply with end"
					update.message.reply_text(message,parse_mode='HTML')
					return ATTLIST

		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def cancel(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				message = "And here I was, thinking we could be friends :("
				update.message.reply_text(message,parse_mode='HTML')
				cur.execute("""DELETE FROM User WHERE telegram_id = %s""",(uid,))
				cur.execute("""DELETE FROM Attribute WHERE telegram_id = %s""",(uid,))
				return ConversationHandler.END


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def forget(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				cur.execute("""SELECT * FROM User WHERE telegram_id = %s""",(uid,))
				if cur.rowcount == 0:
					message = "Can't delete what doesn't exist, man"
					update.message.reply_text(message,parse_mode='HTML')
				else:
					cur.execute("""DELETE FROM User WHERE telegram_id = %s""",(uid,))
					cur.execute("""DELETE FROM Attribute WHERE telegram_id = %s""",(uid,))
					message = "Oh, I'll tell you all about it when I see you again"
					update.message.reply_text(message,parse_mode='HTML')


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def list_cattributes(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				cur.execute("""SELECT * FROM Attribute WHERE telegram_id = %s""",(uid,))
				if cur.rowcount == 0:
					message = "You have no cattributes listed!"
					update.message.reply_text(message,parse_mode='HTML')
				else:
					cattributes = cur.fetchall()
					catlist = [x[1] for x in cattributes]
					message = "".join(['Your current cattributes are: ',(", ".join(catlist))])
					update.message.reply_text(message,parse_mode='HTML')


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def remove_cattributes(self,bot,update,args):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				try:
					cattribute_to_remove = str.lower(args[0])
				except IndexError:
					reply_message = "Can't remove an empty string! Please use the following format: /rmcattributes cattributename" 
					update.message.reply_text(reply_message,parse_mode='HTML')
				else:
					cur.execute("""SELECT * FROM Attribute 
									WHERE telegram_id = %s 
									AND LOWER(attribute_name) = LOWER(%s)
								""",(uid,cattribute_to_remove,))
					if cur.rowcount == 0:
						reply_message = "Can't find that cattribute! please use /listcattributes to show your cattributes"
						update.message.reply_text(reply_message,parse_mode='HTML')
					else:
						cur.execute("""DELETE FROM Attribute 
										WHERE telegram_id = %s
										AND LOWER (attribute_name) = LOWER(%s)
										""",(uid,cattribute_to_remove,))
						reply_message = "".join([str.lower(cattribute_to_remove), " has been sucessfully removed"])
						update.message.reply_text(reply_message,parse_mode='HTML')


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def add_cattributes(self,bot,update,args):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				try:
					cattribute_to_add = str.lower(args[0])
				except IndexError:
					reply_message = "Can't add an empty string! Please use the following format: /addcattributes cattributename" 
					update.message.reply_text(reply_message,parse_mode='HTML')
				else:
					cur.execute("""SELECT * FROM Attribute 
									WHERE telegram_id = %s 
									AND LOWER(attribute_name) = LOWER(%s)
								""",(uid,cattribute_to_add,))
					if cur.rowcount > 0:
						reply_message = "This cattribute is already added!"
						update.message.reply_text(reply_message,parse_mode='HTML')
					else:
						cur.execute("""INSERT INTO Attribute VALUES(%s,%s)""",(uid,cattribute_to_add))
						reply_message = "".join([str.lower(cattribute_to_add)," has been added to the table"])
						update.message.reply_text(reply_message,parse_mode='HTML')


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def alert(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				uid = update.message.from_user.id
				cur.execute("""SELECT * FROM User WHERE telegram_id = %s""",(uid,))
				if cur.rowcount == 0:
					message = "Cant send alerts to you if I don't know who you are, please register!"
					update.message.reply_text(message,parse_mode='HTML')
				else:
					data = cur.fetchone()
					newupdate = ""
					if data[5] == "No":
						newupdate = "Yes"
					else:
						newupdate = "No"
					cur.execute("""UPDATE User SET alert = %s WHERE telegram_id = %s""",(newupdate,uid,))
					message = "Set your alert status to "
					message += newupdate
					update.message.reply_text(message,parse_mode='HTML')


		except Exception as e:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

	def user_broadcast(self,bot,update):
		try:
			with closing(self.conn.cursor()) as cur:
				cur.execute("""SELECT * FROM User WHERE alert = 'Yes'""")
				if cur.rowcount > 0:
					data = cur.fetchall()
					for each in data:
						cur.execute("""SELECT * FROM Attribute WHERE telegram_id = %s""",(each[0]))
						if cur.rowcount > 0:
							print('here')
							attribute_list = []
							att = cur.fetchall()
							for attribute in att:
								attribute_list.append(attribute[1])
							information_list = [each[0],each[1],each[2],each[3],each[4]]
							# tgid,gen,cdindex,offsetst,offsetend
							data_dict = get_Data_Individual().broadcast_user(information_list,attribute_list)
							if data_dict:
								for user,kitten in data_dict.items():
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
									
									try:
										bot.sendMessage(chat_id=each[0],text=message,parse_mode='HTML')
										if "image" in kitten:
											bot.sendPhoto(chat_id=each[0],photo=open(kitten["image"],'rb'))
											os.remove(kitten["image"])
								
									except Exception as e:
										# more timeouts. Im trying to break the habit of doing this, but I cant seem to catch
										# the socket.timeout error that is thrown by telegram's servers even if I explicitly
										# state socket.timeout. Appreciate some help if anyone can help.
										
										# seems like 10 second is the magic number - we'll try that
										os.remove(kitten["image"])
										pass
											
										

		except:
			#All encompassing try excepts are generally not good idea.
			# but I want to be notified in this case.
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=Tokens().error_channel(),text=catcherror,parse_mode='HTML')

