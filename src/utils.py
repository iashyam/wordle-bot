class Functions:
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
