#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitties init.
# Written by xlanor
##

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job, MessageHandler, Filters, RegexHandler, ConversationHandler
from tokens import Tokens
from commands import Commands,GENERATION,COOLDOWN,OFFSTART,OFFEND,ATTLIST

def Cryptokitties():
	print("Cryptokitties online")
	updater = Updater(token=Tokens().bot_token())
	dispatcher = updater.dispatcher
	# registering for users to a database.
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('register', Commands().register)],

		states={
			GENERATION:[MessageHandler(Filters.text,Commands().generation)],
			COOLDOWN:[MessageHandler(Filters.text,Commands().cooldown)],
			OFFSTART:[MessageHandler(Filters.text,Commands().offstart)],
			OFFEND:[MessageHandler(Filters.text,Commands().offend)],
			ATTLIST: [MessageHandler(Filters.text,Commands().attribute_list)]
		},

		fallbacks=[CommandHandler('cancel', Commands().cancel)],
		per_user = 'true'
	)
	dispatcher.add_handler(conv_handler,1)

	forget_handler = CommandHandler('forget', Commands().forget)
	dispatcher.add_handler(forget_handler)

	alert_handler = CommandHandler('alert',Commands().alert)
	dispatcher.add_handler(alert_handler)

	list_handler = CommandHandler('listcattributes',Commands().list_cattributes)
	dispatcher.add_handler(list_handler)

	remove_cattribute = CommandHandler('rmcattributes',Commands().remove_cattributes, pass_args=True)
	dispatcher.add_handler(remove_cattribute)

	add_cattribute = CommandHandler('addcattributes',Commands().add_cattributes, pass_args=True)
	dispatcher.add_handler(add_cattribute)
	########################################################
	#				Alert jobs
	########################################################
	j = updater.job_queue
	# this particular job is for my colleagues and using the def broadcast and broadcast module.
	# to broadcast to channels.
	job_minute = j.run_repeating(Commands().user_broadcast,600,0)
	updater.start_polling()
	updater.idle

if __name__ == '__main__':
	Cryptokitties()