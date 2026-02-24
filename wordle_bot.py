
from numpy import log2 as ln
# from tqdm import tqdm
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
		# Sort by info value in descending order and grab top 5
		top_infos = sorted(infos.items(), key=lambda item: item[1], reverse=True)[:5]
		
		print(f"  {'words':<6} {'infos'}")
		# Mimicking the previous pandas output format
		for i, (word, info) in enumerate(top_infos):
			print(f"{i} {word:<6} {info:.6f}")
	
	def get_valid_input(self, words):
		while True:
			guess = input("Enter the guess: ").lower()
			if len(guess) != 5:
				print("Invalid guess, please try again")
				continue
			if guess not in words:
				print("Word isn't in our list, please try again")
				continue
				
			pattern = input("Enter the pattern: ").upper()
			if not Func.is_valid_pattern(pattern):
				print("Invalid pattern, please try again")
				continue
				
			return guess, pattern

	def solve(self):
		words = Data.words
		for attempts in range(6):
			infos = self.max_info(words)
			self.print_info(infos)
			
			guess, pattern = self.get_valid_input(words)
			
			if pattern == "GGGGG":
				print("congratulations, we did it!")
				break
				
			word_index = words.index(guess)
			words = self.dicts[word_index][pattern]
			print("Remaining Solutions: ", len(words))
			
			if len(words) == 0:
				print("Today's word isn't in our list, tough luck!")
				break

if __name__=="__main__":
	bot = Wordle()
	bot.solve()
