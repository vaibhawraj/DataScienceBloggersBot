#fetchUpdate.py

import sys
import requests
import DataStorageHandler
import datetime
from dateutil.parser import parse as parseDate
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
	retDict = {'items':None, 'blogRec':pollRes['blogRec']}
	if pollRes['status'] == True:
		blogRec = pollRes['blogRec']
		if pollRes['xmlBody'] != None:
			#Start Parsing
			try:
				root = ET.fromstring(pollRes['xmlBody'])
				
				#Need to identify XML Structure
				#For RSS, it must be of Standard structure with channel & items
				channelNode = root.find('channel')
				if channelNode != None:
					titleNode = channelNode.find('title')
					linkNode = channelNode.find('link')
					descriptionNode = channelNode.find('description')
					itemNodeList = channelNode.findall('item')
					
					if titleNode != None:
						retDict['blogRec']['title'] = titleNode.text
					if linkNode != None:
						retDict['blogRec']['link'] = linkNode.text
					if descriptionNode != None:
						retDict['blogRec']['description'] = descriptionNode.text

					items = []
					for itemNode in itemNodeList:
						itemTitleNode = itemNode.find('title') 
						itemLinkNode = itemNode.find('link')
						itemPubNode = itemNode.find('pubDate')
						
						item = {'title':None, 'link':None, 'pubDate':None}
						if itemTitleNode != None:
							item['title'] = itemTitleNode.text
						if itemLinkNode != None:
							item['link'] = itemLinkNode.text
						if itemPubNode != None:
							item['pubDate'] = itemPubNode.text
						items.append(item)
					retDict['items'] = items
					blogRec['status'] = True
				else:
					blogRec['errorMessage'] = 'Improper RSS Structure'
					blogRec['delete'] = True
			except:
				blogRec['errorMessage'] = str(sys.exc_info()[0])
				blogRec['errorCount'] = blogRec['errorCount'] + 1
				if blogRec['errorCount'] > 10:
					blogRec['delete'] = True
		retDict['blogRec'] = blogRec
	return retDict

def pollAll(blogRecList,itemRecList):
	for blogRec in blogRecList:
		if blogRec['delete'] == False:
			pollRes = poll(blogRec)
			parseRes = parseXML(pollRes)
			if parseRes['blogRec']['status'] == True:
				blogRec = parseRes['blogRec']
				firstTime = blogRec['firstTime']
				items = parseRes['items']
				for item in items:
					if item['pubDate'] != None:
						pDate = parseDate(item['pubDate'])
						if firstTime or pDate.date() == datetime.today():
							newItemRec = {}
							newItemRec['title'] = item['title']
							newItemRec['pubDate'] = item['pubDate']
							newItemRec['link'] = item['link']
							newItemRec['blogUrl'] = blogRec['url']
							newItemRec['isNew'] = True
							isExist = False
							for itemRec in itemRecList:
								if itemRec['link'] == newItemRec['link']:
									isExist = True
									break
							if isExist == False:
								itemRecList.append(newItemRec)
				if firstTime:
					blogRec['firstTime'] = False
						
	print(blogRecList)
	print(itemRecList)

def newBlogRec(url):
	blogRec = {'url':url,'errorCount':0,'status':False,'firstTime':True,'delete':False}
	return blogRec

def fetchAllBlogRec():
	pass

def fetchAllItemRec():
	pass

def save
blogRecList = []
blogRec = {'url':'http://blog.smola.org/rss','errorCount':0,'status':False,'firstTime':True,'delete':False}
blogRecList.append(blogRec)
itemRecList = []
pollAll(blogRecList,itemRecList)

