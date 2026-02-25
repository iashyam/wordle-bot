import json
import os
from numpy import log2 as ln
from src.load_data import Data
from src.utils import Functions

Data = Data()
Func = Functions()

class WordleSolver:
	def __init__(self, starting_words=None):
		self.words = starting_words if starting_words else Data.words
		self.dicts = []

	def max_info(self, word_list: list) -> dict:
		infos = {}
		N = len(word_list)
		self.dicts = []
		
		is_first_iteration = (N == len(Data.words))
		cache_file = "data/initial_cache.json"

		# If it's the first iteration and we have a cache, load it directly
		if is_first_iteration and os.path.exists(cache_file):
			with open(cache_file, "r") as f:
				cache_data = json.load(f)
				self.dicts = cache_data["dicts"]
				infos = cache_data["infos"]
			return infos

		#comparing each words and sorting the patterns
		for choice in word_list:
			my_dict = {}

			for ref in word_list:
				pattern = Func.compare_words(choice, ref)
				if pattern not in my_dict.keys():
					my_dict[pattern] = []
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

		# If this is the first iteration, save the computed data to cache
		if is_first_iteration:
			with open(cache_file, "w") as f:
				json.dump({"dicts": self.dicts, "infos": infos}, f)

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
