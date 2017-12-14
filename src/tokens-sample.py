#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitty tokens, usernames, passwords
# Written by xlanor
##
class Tokens():
	def __init__(self):
		self.live = "bot token here"
		self.errorchannel = "error channel here"
		self.host = "host"
		self.usn = "username"
		self.pwd = "password"
		self.db = "Cryptokitties"

	def mysql(self):
		conn_string = {"host":self.host,"user":self.usn,"password":self.pwd,"db":self.db}
		return conn_string

	def bot_token(self):
		return self.live

	def error_channel(self):
		return self.errorchannel
