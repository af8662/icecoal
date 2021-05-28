# -*- coding: utf-8 -*-
import os, sys
from icecoal import query
import string

def create_db(db_name):
	return query("create database {}".format(db_name))

def use_db(db_name):
	pass

def create_table(tb_name, fields):
	return query("create table {}{}".format(tb_name, fields))
	
def create_db_tb():
	results = create_db("students")
	results = create_table("students/course","(name,no,course)")

def select_unicode():
	# q = 'select 系所 from ./EE5178_student_data_2.csv where \"系所\"=\'電機系\''
	q = 'select 身份,系所 from ./EE5178_student_data_1.csv where 身份=\'校內生 \''
	results = query(q)
	print(q)
	print(results)
	sys.exit('a')

def main():
	q = 'select 身份 from ./EE5178_student_data_1.csv where id=3'
	q = 'select 身份,系所 from ./EE5178_student_data_1.csv'
	# q = 'select * from ./EE5178_student_data_1.csv'
	select_unicode()
	
	results = query(q)
	# results = create_db("students")
	# results = create_table("students/course","(name,no,course)")
	print(q)
	print(results)
	
if __name__ == '__main__':
	main()