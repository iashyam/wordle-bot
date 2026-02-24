from numpy import log2 as ln
from src.load_data import Data
from src.utils import Functions

Data = Data()
Func = Functions()

class WordleSolver:
	def __init__(self, starting_words=None):
		self.words = starting_words if starting_words is not None else Data.words
		self.dicts = []

	def max_info(self, word_list: list) -> dict:
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

	def get_best_guesses(self, n=5) -> list:
		"""Returns the top N words with the highest information gain."""
		infos = self.max_info(self.words)
		# Sort by info value in descending order and grab top N
		top_infos = sorted(infos.items(), key=lambda item: item[1], reverse=True)[:n]
		return top_infos

	def update_state(self, guess: str, pattern: str):
		"""Updates the remaining words list based on a given guess and pattern outcome."""
		word_index = self.words.index(guess)
		self.words = self.dicts[word_index][pattern]

	def get_remaining_count(self) -> int:
		"""Returns the number of possible solutions remaining."""
		return len(self.words)
