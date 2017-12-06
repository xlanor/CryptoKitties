#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitties init.
# Written by xlanor
##

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job, MessageHandler, Filters, RegexHandler, ConversationHandler
from tokens import Tokens
from commands import Commands

def Cryptokitties():
	print("Cryptokitties online")
	updater = Updater(token=Tokens.bot_token("live"))
	dispatcher = updater.dispatcher
	j = updater.job_queue
	job_minute = j.run_repeating(Commands.broadcast,150,0)
	job_minute = j.run_repeating(Commands.kleongbroadcast,150,0)
	updater.start_polling()
	updater.idle

if __name__ == '__main__':
	Cryptokitties()