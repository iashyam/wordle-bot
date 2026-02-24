from src.solver import WordleSolver
from src.utils import Functions

Func = Functions()

class WordleCLI:
	def __init__(self):
		self.solver = WordleSolver()

	def print_info(self, top_infos: list):
		print(f"  {'words':<6} {'infos'}")
		for i, (word, info) in enumerate(top_infos):
			print(f"{i+1} {word:<6} {info:.6f}")
	
	def get_valid_input(self):
		while True:
			guess = input("Enter the guess: ").lower()
			if len(guess) != 5:
				print("Invalid guess, please try again")
				continue
			if guess not in self.solver.words:
				print("Word isn't in our list, please try again")
				continue
				
			pattern = input("Enter the pattern: ").upper()
			if not Func.is_valid_pattern(pattern):
				print("Invalid pattern, please try again")
				continue
				
			return guess, pattern

	def start(self):
		for attempts in range(6):
			# Get best guesses and display them
			top_guesses = self.solver.get_best_guesses()
			self.print_info(top_guesses)
			
			# Get validated input
			guess, pattern = self.get_valid_input()
			
			if pattern == "GGGGG":
				print("congratulations, we did it!")
				break
			
			# Ask the solver to update its state based on the actual outcome
			self.solver.update_state(guess, pattern)
			remaining_count = self.solver.get_remaining_count()
			
			print("Remaining Solutions: ", remaining_count)
			if remaining_count == 0:
				print("Today's word isn't in our list, tough luck!")
				break

if __name__=="__main__":
	cli = WordleCLI()
	cli.start()
