#DataStorageHandler.py

import CsvHandler

class DataStorageHandler():

	listOfTables = {}
	def __init__(self):
		pass

	def getTable(tableName):
		listOfTables = DataStorageHandler.listOfTables
		print(listOfTables)
		print(listOfTables.get(tableName))
		if(listOfTables.get(tableName) != None):
			return listOfTables[tableName] 
		else:
			listOfTables[tableName] = 'New Table'
		pass

	def setTable(self, tableName):
		pass

#n = DataStorageHandler.getTable('Apple')
#print(n)
#y = DataStorageHandler.getTable('Apple')
#print(y)
