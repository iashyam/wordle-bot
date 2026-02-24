import pandas as pd
import json
import os

class Data:
	def __init__(self):	
		self.getWords()
		self.patterns = self.getPatterns()
		df = pd.read_csv("data/frequencies.csv")
		self.df = df.set_index('word')

	def getWords(self):

		data = pd.read_csv("data/wordle-allowed-guess.csv")
		# data = pd.read_csv("../data/allowed_words.txt")
		self.words = data["word"].to_list()
	
    #generate all the patterns with three letters GBY
	def generatePatterns(self):
		cache_file = "data/patterns.json"
		if os.path.exists(cache_file):
			with open(cache_file, "r") as f:
				self.lst = json.load(f)
			return

		self.lst = [""]
		for word in self.lst:
			if len(word)<5:
				self.lst.append(word+"B")
				self.lst.append(word+"G")
				self.lst.append(word+"Y")
			else:
				continue

		with open(cache_file, "w") as f:
			json.dump(self.lst, f)

    #filter only the pattern with length 5
	def getPatterns(self):
		import time
		self.generatePatterns()
    	#create a filter 
		filter_function = lambda pattern: len(pattern)==5 
		patterns = list(filter(filter_function, self.lst))
		return patterns

		
