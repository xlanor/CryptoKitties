#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitty Create tables
#
##

import pymysql,traceback
from contextlib import closing
from tokens import Tokens


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
	def create_user_table(self):
		try:
			with closing (pymysql.connect(Tokens.mysql('host'),Tokens.mysql('usn'),Tokens.mysql('pwd'),Tokens.mysql('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					cur.execute(create_user_table_string) #Change cryptokitties to whatever you call your db in tokens.
		except Exception as e:
			catcherror = traceback.format_exc()
			self.write_error(catcherror)
		else:
			self.write_error('User Table Sucessfully created')

	def create_attributes_table(self):
		try:
			with closing (pymysql.connect(Tokens.mysql('host'),Tokens.mysql('usn'),Tokens.mysql('pwd'),Tokens.mysql('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					cur.execute(create_attributes_table_string)
		except Exception as e:
			catcherror = traceback.format_exc()
			self.write_error(catcherror)
		else:
			self.write_error('Attributes table successfully created')

	def write_error(self,error):
		with open('logs.txt','a') as f:
			f.write(str(error))
			f.write(traceback.format_exc())

if __name__ == '__main__':
	CreateDb().create_user_table()
	CreateDb().create_attributes_table()
