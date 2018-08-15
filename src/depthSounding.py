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
#import BeautifulSoup
import json
import matplotlib.pyplot as plt; 
import matplotlib.mlab as mlab;
from sklearn.mixture import GaussianMixture
from sklearn.mixture import BayesianGaussianMixture
from bs4 import BeautifulSoup

__author__ = "Luke Burks"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Luke Burks"
__email__ = "clburks9@gmail.com"
__status__ = "Development"


def makeASounding(data):
	#initialize
	session = requests.session(); 
	req = session.get('https://en.wikipedia.org/wiki/Special:Random'); 
	#req = session.get('https://en.wikipedia.org/wiki/Polity')
	doc = BeautifulSoup.BeautifulSoup(req.content); 

	maxDepth = 100; 

	titlePath = [];
	allLinksVisited = []; 
	fixedTitle = str(doc.title).replace("<title>","").replace(" - Wikipedia</title>","");
	#print(fixedTitle)
	




	for i in range(0,maxDepth):
		#get title of doc
		fixedTitle = str(doc.title).replace("<title>","").replace(" - Wikipedia</title>","");
		#if the page hasn't been logged yet
		if(fixedTitle not in data):
			data[fixedTitle] = 0; 
			#all other in title path add 1
			for j in range(0,len(titlePath)):
				data[titlePath[j]] += 1; 
		elif(fixedTitle=='Reality' or fixedTitle == 'Existence'):
			#all other in title path add 1
			for j in range(0,len(titlePath)):
				data[titlePath[j]] += 1;  
		else:
			#add data[fixedTitle] to all in path
			for j in range(0,len(titlePath)):
				data[titlePath[j]] += data[fixedTitle]; 
			return titlePath,data; 0

		titlePath.append(fixedTitle); 
		if(fixedTitle == 'Philosophy'):
			break; 

		#get link name

		try:
			count = 0; 
			firstLink = None; 
			n=0;
			while(firstLink is None and count < 3): 
				
				count+=1; 
				temp = doc.body.findAll('p')[n];
				
				#print(fixedTitle.split(' '))
				while('<b>{}</b>'.format(fixedTitle) not in str(temp) and '<b>{}</b>'.format(fixedTitle).lower() not in str(temp) and fixedTitle.split(' ')[0] not in str(temp) and fixedTitle.split(' ')[0].lower() not in str(temp) or 'Geographic coordinate system' in str(temp) or "Outline_of_Bible-related_topics" in str(temp) or "outline" in str(temp).lower()):
					#print('<b>{}</b>'.format(fixedTitle) )
					#print(temp)
					temp =doc.body.findAll('p')[n];
					n+=1; 
				
				#print(doc); 
				firstLink = temp.findNext('a'); 
				#print(firstLink)
				while("Citation" in str(firstLink) or '#endnote' in str(firstLink) or 'index' in str(firstLink) or "#CITEREF" in str(firstLink) or 'Ancient Greek' in str(firstLink) or firstLink in allLinksVisited or 'link' in str(firstLink) or 'latin' in str(firstLink).lower() or 'language' in str(firstLink) or "#cite" in str(firstLink) or "Help" in str(firstLink) or "upload" in str(firstLink) or "File" in str(firstLink) or 'redirect' in str(firstLink) or 'wiktionary' in str(firstLink) or "English" in str(firstLink)):
					temp=temp.next;
					#print(temp)
					firstLink = temp.findNext('a');
					
			
				#print(firstLink);
				if(firstLink is None or firstLink.string is None):
					firstLink = None;
					n+=1;

		except(AttributeError,IndexError):
			titlePath.append("NULL")
			#change everything in title path to -10; 
			for j in range(0,len(titlePath)):
				data[titlePath[j]] = -10; 

			return titlePath,data;

		#make url
		#print(firstLink.string);
		allLinksVisited.append(firstLink); 
		try:
			ur = 'https://en.wikipedia.org'+firstLink['href'];
		except(TypeError):
			titlePath.append("NULL");
			for j in range(0,len(titlePath)):
				data[titlePath[j]] = -10; 
			return titlePath,data; 

		ur = ur.replace(' ','_')
		#print(ur);
		#print(""); 

		#click on it
		try:
			req = session.get(ur); 
		except(requests.exceptions.ConnectionError):
			titlePath.append("NULL");
			for j in range(0,len(titlePath)):
				data[titlePath[j]] = -10; 	
			return titlePath,data; 

		doc = BeautifulSoup.BeautifulSoup(req.content); 

	return(titlePath,data); 


def plotData(data):
	b = data.values(); 
	a = filter(lambda c: c!=-10,b); 

	print("Length:{}".format(len(a))); 
	print("Mean:{}".format(np.mean(a))); 
	print("SD:{}".format(np.std(a))); 

	num_bins=max(a);
	plt.hist(a,num_bins,facecolor='blue',alpha=0.5,range=(0,max(a)),rwidth=.9); 
	x = np.linspace(min(a),max(a),100); 
	scale = len(a);
	plt.plot(x,mlab.normpdf(x,np.mean(a),np.std(a))*scale,'--k',linewidth=2); 


	
	b = np.zeros(shape = (len(a),1)); 
	for i in range(0,len(a)):
		b[i][0] = a[i]; 
		#b[i][1] = 1; 

	gm = BayesianGaussianMixture(4,max_iter = 1000,n_init = 10); 
	gm.fit(b);

	# models = [None for i in range(1,4)]; 
	# for i in range(1,4):
	# 	models[i-1] = BayesianGaussianMixture(i);
	# 	models[i-1].fit(b);  

	# AIC = [m.aic(b) for m in models]; 
	# BIC = [m.bic(b) for m in models]; 

	# gm = models[np.argmin(AIC)]; 

	means = gm.means_.T.tolist()[0]; 
	covariances = gm.covariances_.T.tolist()[0][0];
	weights = gm.weights_.tolist();  

	gmPlot = np.zeros(len(x)); 
	for i in range(0,2):
		gmPlot = gmPlot + mlab.normpdf(x,means[i],np.sqrt(covariances[i]))*weights[i]*scale; 
	plt.plot(x,gmPlot,'-k',linewidth=2); 

	plt.legend(['Normal Fit','GM Fit','Data'])
	plt.xlabel("First-link distance"); 
	plt.ylabel("Number of pages"); 
	plt.title("First-link distance of Wikipedia pages from Philosophy"); 
	plt.xlim(0,max(a)); 
	plt.show();



def kickStart(fileName):
	print("Kick Starting file path:{}".format(fileName)); 
	path,data = makeASounding({});
	print(path); 
	print(""); 

	di = {}; 
	for i in range(0,len(path)):
		di[path[i]] = len(path)-i; 

	with open(fileName,"w") as f:
		json.dump(di,f); 

def soundItOut(fileName,numIter=100):
	print("Sounding on file path:{}".format(fileName)); 
	with open(fileName) as f:
		data = json.load(f); 
	
	for i in range(0,numIter):
		path,data = makeASounding(data);
		#print(i,path[0],path[-1]); 
		print(i); 

		with open(fileName,"w") as f:
			json.dump(data,f);
	

def loadOnly(fileName):
	print("Loading data for file path:{}".format(fileName)); 
	with open(fileName) as f:
		data = json.load(f); 
	return data; 

if __name__ == '__main__':

	fileName = '../data/dataset1.json';
	#kickStart(fileName); 
	#soundItOut(fileName,1000); 

	data = loadOnly(fileName); 
	#plotData(data); 

	#b = data.values(); 
	#a = filter(lambda c: c!=-10,b); 

	print(sorted(data,key=data.get));
