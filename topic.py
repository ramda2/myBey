#!/usr/bin/env python2
# Topic Modeling Libraries
import pandas as pd
from gensim import corpora, models, similarities, matutils

# Web framework
from flask import Flask, request
from flask.ext.cors import CORS

import json
from operator import itemgetter
import pprint
import random
import re

# pretty printer for inspecting stuff in this program
# usage pp.pprint(<variable_name>)
pp = pprint.PrettyPrinter()

number_topics=7

def getStopWords(stopList='stoplist-multilingual.txt'):
	stop=[]
	with open(stopList) as f:
		stop=f.readlines()
		stop=[word.strip('\n') for word in stop]
	return stop

def getLines(lyrics='lyrics.txt'):
	test = []
	with open(lyrics) as f:
		test = json.load(f)
		test = map(lambda x: str(x), test)  # unicode 'python2 vs json' woes
	our_texts = test  # variable names...

	return our_texts

stop = getStopWords()
our_texts = getLines()

# turn into multidimensional array and skip stop words
texts = [[word for word in document.lower().split() if word not in stop] for document in our_texts]
dictionary = corpora.Dictionary(texts)

def data_cleanse(docs_to_clean):
	D=len(docs_to_clean)
	for d in range(0, D):
	    docs_to_clean[d] = docs_to_clean[d].lower()
	    docs_to_clean[d] = re.sub(r'[-\[\]]', ' ', docs_to_clean[d]) #ask 
	    docs_to_clean[d] = re.sub(r'[^a-zA-Z0-9 ]', '', docs_to_clean[d])
	    docs_to_clean[d] = re.sub(r' +', ' ', docs_to_clean[d])
	    docs_to_clean[d] = re.sub(r'\s\w\s', ' ', docs_to_clean[d]) #eliminate single letters
	return docs_to_clean

def create_model():
	data_cleanse(our_texts)

	"""gensim includes its own vectorizing tools"""
	corpus = [dictionary.doc2bow(text) for text in texts]

	#use gensim multicore LDA
	model = models.LdaModel(corpus, id2word=dictionary, num_topics=number_topics, passes=10)
	model.save('ldabey')
	model.show_topics()

	topics_indexed=[[b for (a,b) in topics] for topics in model.show_topics(number_topics,10,formatted=False)]
	topics_indexed=pd.DataFrame(topics_indexed)
	pp.pprint(topics_indexed)

model = models.LdaModel.load('ldabey', mmap='r')
# model.show_topics()

# couldnt get this list comprehension to work on my machine: 
# topics_indexed=[[b for (a,b) in topics] for topics in model.show_topics(number_topics,10,formatted=False)]
topics_indexed = [topic for topic in model.show_topics(number_topics,10,formatted=False)]
ti = []
for topic in topics_indexed:  # topics_indexed = [b for (a,b) in topic]
	a, b = topic
	print b
	ti.append(b)
topics_indexed = ti

topics_indexed=pd.DataFrame(topics_indexed)

topic_map = [[], [], [], [], [], [], []]
for o in our_texts:
	try:
		results = model[dictionary.doc2bow(o.lower().split()) ]
		value = max(results,key=itemgetter(1))[0] 
		topic_map[value].append(o)
	except Exception, e:
		continue

app = Flask(__name__)

@app.route('/status', methods = ['POST'])
def getStatus():
	line = str(request.form['textmessage'])
	try:
		results = model[dictionary.doc2bow(line.lower().split()) ]
		value = max(results,key=itemgetter(1))[0] 
		message = random.choice (topic_map[value])
		#0-coquettish 1-coquettishplus 2-upset 3-dance 4-romance 5-angry 6-carefree
		if(value == 0):
			gif = 'coquettish'
		elif(value == 1):
			gif = 'coquettishplus'
		elif(value == 2):
			gif = 'upset'
		elif(value == 3):
			gif = 'dance'
		elif(value == 4):
			gif = 'romance'
		elif(value == 5):
			gif = 'angry'
		elif(value == 6):
			gif = 'carefree'
		return json.dumps({'message': message, 'gif': gif})
	
	except Exception, e:
		message = random.choice (our_texts)
		return json.dumps({'message': message, 'gif': 'default'})

# pp.pprint(topics_indexed)

if __name__ == "__main__":
	CORS(app)
	app.run(debug=True)
