#fetchUpdate.py

import sys
import requests
import DataStorageHandler
import xml.etree.ElementTree as ET
#Get List of Blogs
#Start Polling
#	If Its a first Time, then Add All
#	OtherWise Add todays Blog only, marked Unread

def poll(blogRec):
	#blogRec is a dictionary
	url = blogRec['url']
	xmlBody = None
	statusFlag = True
	try:
		res = requests.get(url)
		status = res.status_code
		if status == requests.status_codes.codes.OK:
			xmlBody = res.text
			statusFlag = True
		else:
			if status == requests.status_codes.codes.not_found:
				blogRec['delete'] = True
			blogRec['errorCount'] = blogRec['errorCount'] + 1
			blogRec['errorMessage'] = status
			statusFlag = False
	except:
		print(sys.exc_info()[0])
		blogRec['errorCount'] = blogRec['errorCount'] + 1
		blogRec['errorMessage'] = str(sys.exc_info()[0])
		statusFlag = False
	if blogRec['errorCount'] > 10:
		blogRec['delete'] = True
	return {'xmlBody':xmlBody,'blogRec':blogRec,'status':statusFlag}

def parseXML(pollRes):
	#parseXML will parse pollRes XML and return dictionary with blog Title, Link, List of Items
	retDict = {'title':None,'link':None,'description':None,'items':None}
	if pollRes['status'] == True:
		blogRec = pollRes['blogRec']
		if pollRes['xmlBody'] != None:
			#Start Parsing
			try:
				root = ET.fromString(pollRes['xmlBody'])
				#Need to identify XML Structure
				#For RSS, it must be of Standard structure with channel & items
				channelNode = root.find('channel')
				if channelNode != None:
					titleNode = channel.find('title')
					linkNode = channel.find('link')
					descriptionNode = channel.find('description')
					itemNodeList = channel.findAll('item')
					
					if titleNode != None:
						retDict['title'] = titleNode.text
					if linkNode != None:
						retDict['link'] = linkNode.text
					if descriptionNode != None:
						retDict['description'] = descriptionNode.text

					items = []
					for itemNode in itemNodeList:
						itemTitleNode = itemNode.find('title') 
						itemLinkNode = itemNode.find('link')
						itemPubNode = itemNode.find('pubDate')
						
						print(itemPubNode.text)
						item = {'title':None, 'link':None, 'pubDate':None}

				else:
					blogRec['errorMessage'] = 'Improper RSS Structure'
					blogRec['delete'] = True
			except:
				blogRec['errorMessage'] = str(sys.exc_info()[0])
				blogRec['errorCount'] = blogRec['errorCount'] + 1
				if blogRec['errorCount'] > 10:
					blogRec['delete'] = True
			
blogRec = {'url':'http://www.google.com','errorCount':0}
pollRes = poll(blogRec)
print(blogRec)
