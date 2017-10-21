'''
************************************************************************************************************************************************************
File: depthSounding.py
Written By: Luke Burks
October 2017

Objectives:
1. Testing the claim that recursivly clicking the first link in wikipedia
pages will inevitably lead to the page for philosophy
2. Finding the expected number of recursive clicks to reach philosophy

************************************************************************************************************************************************************
'''

from __future__ import division
import numpy as np
import requests
import BeautifulSoup


__author__ = "Luke Burks"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Luke Burks"
__email__ = "clburks9@gmail.com"
__status__ = "Development"


def makeASounding():
	#initialize
	session = requests.session(); 
	req = session.get('https://en.wikipedia.org/wiki/Special:Random'); 
	doc = BeautifulSoup.BeautifulSoup(req.content); 

	maxDepth = 10; 

	titlePath = [];

	for i in range(0,maxDepth):
		#get title of doc
		fixedTitle = str(doc.title).replace("<title>","").replace(" - Wikipedia</title>","");
		titlePath.append(fixedTitle); 
		if(fixedTitle == 'Philosophy'):
			break; 

		#get link name
		firstLink = doc.findAll('p')[0].findAll('a')[0]; 

		#make url
		print(firstLink);
		ur = 'https://en.wikipedia.org/wiki/'+firstLink.string;
		ur = ur.replace(' ','_')

		#click on it
		req = session.get(ur); 
		doc = BeautifulSoup.BeautifulSoup(req.content); 

	print(titlePath); 


if __name__ == '__main__':
	makeASounding()