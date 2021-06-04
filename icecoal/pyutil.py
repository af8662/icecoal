# -*- coding: utf-8 -*-
import os
from .icecoal import query, execute_query
from .utilfuns import __select
from .const import *

CURRENT_DB=""

def create_db(db_name):
	return query("create database {}".format(db_name))

def use_db(db_name):
	if not os.path.isdir( os.path.join('.',db_name)):
		raise Exception('database {} is not exist'.format(db_name))
	global CURRENT_DB
	CURRENT_DB = db_name+"/"

def create_table(tb_name, fields):
	tb_name = CURRENT_DB+tb_name
	return query("create table {}{}".format(tb_name, fields))
	
def insert_to_table(tb_name, values):
	assert type(values) == list, 'parameter values should be a list of tuple'
	tb_name = CURRENT_DB+tb_name
	success = 0
	for v in values:
		r = query("insert into {}{}".format(tb_name, str(v)))
		if r[0]==0: # no error occur
			success += 1
		else:
			return r
	return '{} rows inserted'.format(success)
	
def select_header_from_table(tb_name):
	tb_name = CURRENT_DB+tb_name
	r = query("select * from {}, {}".format(tb_name,tb_name))
	if r[0] != 0:
		raise Exception(r)
	return r[2][0]
	
def select_from_where(fields, tb_names, where=""):
	def _permutation(all, query_results):
		if query_results == []:
			return all
		rows = query_results.pop(0)[2]
		if all == []:
			new = rows
		else:
			new = []
			for row in rows:
				for a in all:
					new_r = a[:]
					new_r.extend(row)
					new.append(new_r)
		
		return _permutation(new, query_results)
	
	if type(fields) is str:
		fields = fields.split(',')
	if type(tb_names) is str:
		tb_names = tb_names.split(',')
		
	tb_titles = [select_header_from_table(tb) for tb in tb_names]
	all_titles = []
	for t in tb_titles:
		all_titles.extend(t)
		
	selectf = [[] for _ in tb_names]		
	if fields == ['*']:
		selectf = tb_titles
	else:
		for f in fields:
			found = 0
			for i, tb in enumerate(tb_titles):
				if f in tb:
					found += 1
					selectf[i].append(f)
			if found == 0:
				return [-11, 'No field {} found in header'.format(f), []]
			elif found > 1:
				return [-1, " Column '{}' in field list is ambiguous".format(f), []]	
	query_results = []
	for i,_ in enumerate(selectf):
		a = '*'
		b = CURRENT_DB+tb_names[i]
		query_results.append(query('select {} from {}'.format(a,b)))
	all_permutations = _permutation([], query_results)
	
	if type(where) is str:
		where = where.replace('and','AND')
		where = where.split('AND')
	for i in range(len(where)-1):
		all_permutations = _filter(all_titles, all_permutations, all_titles, where=where[i])
		all_permutations = all_permutations[2]		
	results = _filter(fields, all_permutations, all_titles, where=where[-1])	
	return results
	
def _filter(selectf, all_permutations, all_titles, where=""):
	etree = execute_query(where, return_etree=True)
	rows = [DELIMITER.join(r) for r in all_permutations]
	return __select(selectf, rows, all_titles, etree, from_csvfile=False)
		