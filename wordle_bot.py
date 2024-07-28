import pandas as pd
from numpy import log2 as ln
from tqdm import tqdm

class wordle:
	def __init__(self):
		self.get_words()
		self.patterns = self.get_patterns()
		df = pd.read_csv("frequencies.csv")
		self.df = df.set_index('word')

	def get_words(self):
		data = pd.read_csv("wordle-allowed-guess.csv")
		# data = pd.read_csv("allowed_words.txt")

		self.words = data["word"].to_list()

	def get_probabilities(self, thing):
		return self.df.loc[thing]['prob'].sum()

	#create a list of patterns
	def get_patterns(self):
		lst = [""]
		
		for word in lst:
			if len(word)<5:
				lst.append(word+"B")
				lst.append(word+"G")
				lst.append(word+"Y")
			else:
				continue

		list2 = []
		for word in lst:
			if len(word)==5:
				list2.append(word)

		return list2

	#compare two words and get pattern
	def compare_words(self, check, ref):
		check = check.upper()
		ref = ref.upper()

		pattern = ""
		for i in range(5):
			letter = check[i]
			if letter not in ref:
				pattern += "B"
			elif letter in ref:
				if ref[i]==letter:
					pattern += "G"
				else:
					if letter in check[:i]:
						pattern += "B"
					else:
						pattern += "Y"
		return pattern 


		#get the next most probable words:
	def max_info(self, word_list):
		infos = {}
		N = len(word_list)
		self.dicts = []

			#comparing each words and sorting the patterns
		for choice in word_list:
			my_dict = {}
			for i in range(len(self.patterns)):
				my_dict[self.patterns[i]]=[]

			for ref in word_list:
				pattern = self.compare_words(choice, ref)
				my_dict[pattern].append(ref)

			self.dicts.append(my_dict)

			#computing the information based on the length of pattern groups

		for i in range(N):
			dict_ = self.dicts[i]
			vals = list(dict_.values())
			info = 0
			for j in range(len(vals)):
				if len(vals[j])!=0:
					# omega = self.get_probabilities(vals[j])
					omega = len(vals[j])/N
					info -= omega*ln(omega)
			infos[word_list[i]] = info

		return infos


	def print_info(self, infos):
	
		infos_df = pd.DataFrame(list(infos.items()))
		infos_df.columns=["words", "infos"]
		infos_df = infos_df.sort_values(by="infos", ascending=0)
		print(infos_df.head())
	
	def solve(self):
		words = self.words
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
	bot = wordle()
	bot.solve()
