from myapp import app, mysql
import numpy as np
from flask import url_for

class Details:
	def __init__(self):
		pass

	def get_details(self,table_name, image_name):
		conn = mysql.connect()
		cursor = conn.cursor()
		image_path = ''
		image_name = str(image_name)
		print image_name
		if table_name == 'lung_l':
			image_path = '/static/train_l/'+image_name
			cursor.execute("select * from lung_l_details where image_name = '%s'"%image_name)
		elif table_name == 'lung_m':
			image_path = '/static/train_m/'+image_name
			cursor.execute("select * from lung_m_details where image_name = '%s'"%image_name)
		
		res_fetch = cursor.fetchall()
		res_list = []
		res_list.append(image_path)
		res_list.append(res_fetch)
		cursor.close()
		conn.close()
		return res_list