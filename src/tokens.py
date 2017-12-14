#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitty tokens, usernames, passwords
# Written by xlanor
##
class Tokens():
	def __init__(self):
		self.live = "dummy" # a dummy bot token I found online so that telegram wont throw an exception and allow travis to build
		self.errorchannel = "dummy" # a dummy private channel I created so that telegram wont throw an exception and allow travis to build
		self.host = "localhost" #travis db
		self.usn = "root"  #travis db
		self.pwd = ""	#travis db
		self.db = "Cryptokitties"
		self.charset = "utf-8"

	def mysql(self):
		conn_string = {"host":self.host,"user":self.usn,"password":self.pwd,"db":self.db}
		return conn_string

	def bot_token(self):
		return self.live

	def error_channel(self):
		return self.errorchannel


