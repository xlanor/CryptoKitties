#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitty tokens, usernames, passwords
# Written by xlanor
##
class Tokens():
	def bot_token(x):
		if x == "live":
			return '<enter your token>'

	def channel(x):
		if x == "errorchannel":
			return "<enter error channel id>"
		elif x == "livechannel":
			return "<enter live channel id>"

	def mysql(x):
		if x == "host":
			return "dbip"
		elif x == "usn":
			return "dblogin"
		elif x == "pwd":
			return "dbpw"
		elif x == "db":
			return "dbname"