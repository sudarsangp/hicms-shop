from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback


import datetime
import json

class ToJson(object):
	def __init__(self):
		self.storageObject = StorageClass()

	def retJSON(self):
		list1 = list()
		list2 = list()

		for row in session.query(Products).all():
			temp = row.currentStock + row.displayQty
			data_stock = {'Barcode' : row.barcode , 'ShopId' : '5' , 'Stock' : temp}
			list1.append(data_stock)
		for row1 in session.query(Products),all():
			temp1 = session.query(func.avg(Products.price)).filter(Products.barcode = row1.barcode)
			temp2 = session.query(Transaction.unitSold).filter(Transaction.barcode = row1.barcode and Transaction.transactionDate = datetime.datetime.now().date())
			data_soldstock = {'Barcode' : row1.barcode, 'priceSold' : temp1, 'unitSold' : temp2, 'ShopId' : '5'}
			list2.append(data_soldstock)

		final_json = {'Stock' : list1, 'SoldStock' : list2}
		return final_json