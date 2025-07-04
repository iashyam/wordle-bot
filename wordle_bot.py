import pandas as pd
from numpy import log2 as ln
from tqdm import tqdm
from src import *

class Wordle:
	
	#get the next most probable words:
	def max_info(self, word_list: list):
		infos = {}
		N = len(word_list)
		self.dicts = []

		#comparing each words and sorting the patterns
		for choice in word_list:
			my_dict = {pattern: list() for pattern in Data.patterns}

			for ref in word_list:
				pattern = Func.compare_words(choice, ref)
				my_dict[pattern].append(ref)

			self.dicts.append(my_dict)

		#computing the information based on the length of pattern groups
		for i in range(N):
			dict_ = self.dicts[i]
			vals = list(dict_.values())
			info = 0
			for j in range(len(vals)):
				if len(vals[j])!=0:
					omega = len(vals[j])/N
					info -= omega*ln(omega)
			infos[word_list[i]] = info

		return infos


	def print_info(self, infos: dict):
	
		infos_df = pd.DataFrame(list(infos.items()))
		infos_df.columns=["words", "infos"]
		infos_df = infos_df.sort_values(by="infos", ascending=0)
		print(infos_df.head())
	
	def solve(self):
		words = Data.words
		for i in range(6):
			infos = self.max_info(words)
			self.print_info(infos)
			guess = input("Enter the guess: ").lower()
			pattern = input("Enter the pattern: ").upper()
			if pattern=="GGGGG":
				print("congratulations, we did it!")
				break;
			word_index =words.index(guess)
			words = self.dicts[word_index][pattern]
			print("Remaining Solutions: ", len(words))

if __name__=="__main__":
	bot = Wordle()
	bot.solve()
