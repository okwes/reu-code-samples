# Wesley Smith
# Febuary 2024

# This code is from a recent assignment in a computer security class I am currently taking. 
# In it, we were asked to perform a ciphertext-only attack on a vigenere cipher

# The following file provides a series of functions that are useful in the analysis of a vigenere cipher. 
# This file is not intended to be run independently but instead loaded inside of the Python interpreter
# where the functions can be independently called. I also attached the written part of the assignment which asked why I 
# went about my approach and how to effectively use the tools I created.

# For use as a code sample I added an example_use() function which shows off some of the files functionality
# It requires the ciphertext.txt file which I provided to be in the program's working directory

# accepts ciphertext and a desired shift and performs a caesar cipher
def caesar(ciphertext: str, shift: int) -> str:
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	shifted_alphabet = alphabet[shift % len(alphabet):] + alphabet[:shift % len(alphabet)]
	text = []
	for v in ciphertext:
		if v.casefold() in alphabet:
			text.append(shifted_alphabet[alphabet.index(v.casefold())])
		else:
			text.append(v)
	
	return(''.join(text))

# Decodes vigenere cipher once we know the key
# Takes ciphertext and key, both as strings
def devc(ciphertext: str, key: str) -> str:
	text = []
	for i, l in enumerate(ciphertext):
		text.append(caesar(l,  (ord(key[(i % len(key))].casefold())-97)*-1)) # -97 has lowercase a be 0

	return(''.join(text))

# Accepts 
# NOTE assumes just letters, calculation will be off if numbers used
def ioc(text: str) -> float:
	text = ''.join([i for i in text if i.isalpha()])
	freq = [0] * 26
	for l in text:
		freq[ord(l.casefold())-97] = freq[ord(l.casefold())-97] + 1 # add 1 to freq of that letter

	ioc = 0.0
	for i in range(0, 26):
		ioc+= freq[i]*(freq[i]- 1)
	return(ioc/(len(text)*(len(text)-1)))

# takes string and int, returns array of len with letters places in these buckets.
# this is needed as in a vigenere cipher these buckets will all have the same shift
def bucket(text: str, len: int) -> list[str]:
	groups = [""]*len
	for i, l in enumerate(text):
		groups[i % len] += l # appends letter to bucket
	
	return(groups)

# takes text and prints the ioc for diffrent lengths. int is upper lemit on
# max is how many diffrent keylegnths to test
def ioc_rainbow(text: str, max: int) -> None:
	for i in range (1, max + 1):
		print(f"IoCs if key len is {i}: ", end = '')
		for a_bucket in bucket(text, i):
			print(round(ioc(a_bucket), 4), end = ", ")
		print()

# Fairly simple algorythem to get the letter that occurs the most as that should be e in english
# besides looking at just the current letter we add 15 which if e should be t which is seccond most common english letter,
# again than then + 22 which would be a the third most common than compare which occured most
def optimal_key(buckets: list[str]) -> str:
	key = []
	for text in buckets:
		rate = 0
		mostCommon = 'A'
		for l in range(65, 91):
			# chr(((l + 15 - 65) % 26 ) + 65) <- gets letter shifted by 15. -65 is present as we need to start at 0 so we can wrap arround the alphabit with mod
			freq = text.count(chr(l)) + text.count(chr(((l + 15 - 65) % 26 ) + 65)) + text.count(chr(((l + 22 - 65) % 26 ) + 65)) + text.count(chr(((l + 10 - 65) % 26 ) + 65))
			if (freq > rate):
				mostCommon = chr(((l- 65 + 22)  % 26) + 65)
				rate = freq
		key.append(mostCommon)
	return(''.join(key))

# Sample usecase of the functions above. Expects a file ciphertext.txt
# This should be the ciphertext I provided as some of the steps are not purely automated 
def example_use():
	with open('ciphertext.txt', 'r') as file:
		ciphertext = file.read().rstrip()

	print(f"The following is our ciphertext: {ciphertext}\n")

	print("Lets get the IoC or Index of coincidence of the text for various key lengths")
	ioc_rainbow(ciphertext, 11)
	print("The IoC of perfectly distributed text would be 0.0385, but for English it is 0.067\n")

	print("Based on what we saw there the key length is likely 9. Now using the letter frequencies of english we can get some shift and make a probable key")
	bucketed_text = bucket(ciphertext, 9)
	opt_key = optimal_key(bucketed_text)
	print(f"Our most probable key is: {opt_key}\n")
	print(f"Using that our text is as follows: {devc(ciphertext, opt_key)}\n")
	print(f"However, that is not quite right! using some intuition we can guess the key is 'marktwain' and get the following text: {devc(ciphertext, "marktwain")}")

example_use()