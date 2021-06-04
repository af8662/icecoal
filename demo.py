# -*- coding: utf-8 -*-
import os, sys
from icecoal import query
from icecoal.pyutil import *

def insert_data():
	def create_tbl_Anime():
		create_table('tbl_Anime.csv', '(AnimeID,title,officialTitle,type)')
		values = [	('1','Domestic Girlfriend', 'ドメスティックな彼女', 'TV Series'),
					('2','A Certain Scientific Railgun', 'とある科学の超電磁砲', 'TV Series'),
					('3','K-On!', 'けいおん！', 'TV Series')]
		results = insert_to_table('tbl_Anime.csv', values)
		print(results)
	def create_tbl_Creator():
		create_table('tbl_Creator.csv', '(CreatorID,name,officialName,gender,birth)')
		values = [	('1','Maaya Uchida','内田 真礼','female','1989-12-27'),
					('2','Yōko Hikasa','日笠 陽子','female','1985-07-16'),
					('3','Rina Satō','佐藤 利奈','female','1981-05-02'),
					('4','Aki Toyosaki','豊崎 愛生','female','1986-10-28')]
		results = insert_to_table('tbl_Creator.csv', values)
		print(results)
	def create_tbl_Character():
		create_table('tbl_Character.csv', '(CharacterID,name,officialName,gender,CVID)')
		values = [	('1','Rui Tachibana','橘 瑠衣','female','1'),
					('2','Hina Tachibana','橘 陽菜','female','2'),
					('3','Mikoto Misaka','御坂 美琴','female','3'),
					('4','Kazari Uiharu','初春 飾利','female','4'),
					('5','Yui Hirasawa','平沢 唯','female','4'),
					('6','Mio Akiyama','秋山 澪','female','2')]
		results = insert_to_table('tbl_Character.csv', values)
		print(results)
		
	state = create_db('AnimeDB')
	use_db('AnimeDB')
	if state[0] == -15: # Database already exists
		return
	create_tbl_Anime()
	create_tbl_Creator()
	create_tbl_Character()
	
def select_unicode():
	print('\n\n\n----------  select_unicode  ----------')
	q = "select 身份,系所 from ./EE5178_student_data_1.csv where 身份='校內生 '"
	results = query(q)
	print(q)
	print(results)
	
def select_from_single():
	print('\n\n\n----------  select_from_single  ----------')
	use_db('AnimeDB')
	results = select_from_where(['AnimeID'],['tbl_Anime.csv'], where="")
	print(results)

def select_from_multi():
	print('\n\n\n----------  select_from_multi  ----------')
	use_db('AnimeDB')
	# select with python list
	results = select_from_where(['AnimeID', 'CharacterID'],['tbl_Anime.csv','tbl_Character.csv'], ["AnimeID = CharacterID","AnimeID > 1","AnimeID = 2"])
	print(results)
	
	# select with string
	results = select_from_where("AnimeID,CharacterID","tbl_Anime.csv,tbl_Character.csv", "AnimeID = CharacterID and AnimeID > 1 and AnimeID = 2")
	print(results)
	
	# select * without condition, which will return all the permutations
	results = select_from_where('*','tbl_Anime.csv,tbl_Character.csv', where="")
	print(results)
	
def main():
	select_unicode()
	
	insert_data()
	select_from_single()
	select_from_multi()

	
if __name__ == '__main__':
	main()