#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitty Create tables
#
##

import pymysql,traceback
import logging
from contextlib import closing
from tokens import Tokens

logging.basicConfig(filename="createdb.log", level=logging.DEBUG)

create_user_table_string = """
							CREATE TABLE IF NOT EXISTS Cryptokitties.User (
								telegram_id INT(15) NOT NULL,
								generation_index INT(5) NULL,
								cooldown_index INT(5) NULL,
								offset_start INT(5) NULL,
								offset_end INT(5) NULL,
								alert VARCHAR(50) NULL,
								PRIMARY KEY (telegram_id)
								)
							"""
create_attributes_table_string = """
									CREATE TABLE IF NOT EXISTS Cryptokitties.Attribute (
										telegram_id INT(15),
										attribute_name VARCHAR(50)
										)
								"""
class CreateDb():
	def __init__(self):
		token_list = Tokens().mysql()
		self.conn = pymysql.connect(**token_list)
		self.conn.autocommit(True)

	def create_user_table(self):
		try:
			with closing(self.conn.cursor()) as cur:
				cur.execute(create_user_table_string) #Change cryptokitties to whatever you call your db in tokens.

		except Exception as e:
			catcherror = traceback.format_exc()
			self.write_error(catcherror)

		else:
			self.write_error('User Table Sucessfully created')

	def create_attributes_table(self):
		try:
			with closing(self.conn.cursor()) as cur:
				cur.execute(create_attributes_table_string)

			conn.close()
		except Exception as e:
			catcherror = traceback.format_exc()
			self.write_error(catcherror)
		else:
			self.write_error('Attributes table successfully created')

	def write_error(self,error):
		logging.debug(error)

if __name__ == '__main__':
	CreateDb().create_user_table()
	CreateDb().create_attributes_table()
