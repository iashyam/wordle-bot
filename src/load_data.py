import pandas as pd

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
		
		self.lst = [""]
		for word in self.lst:
			if len(word)<5:
				self.lst.append(word+"B")
				self.lst.append(word+"G")
				self.lst.append(word+"Y")
			else:
				continue

    #filter only the pattern with length 5
	def filterPatterns(self):
		
		self.generatePatterns()
    	#create a filter 
		filter_function = lambda pattern: True if len(pattern)==5 else False

		return list(filter(filter_function, self.lst))

    
	def getPatterns(self):
		return self.filterPatterns()
	    

		
