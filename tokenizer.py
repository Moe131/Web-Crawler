import sys


# Time complexity of this method is constant O(1) because it only
# iterates through a constant sized string
def isAlphaNum(ch:str) -> bool:
    ''' Checks if a character is number or american letter  '''
    english_letters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if ch in english_letters:
        return True
    else:
        return False


# Time complexity of this method is linear  O(n) if n is 
# the number of 100bytes in file. The method iterates through 
# the characters(bytes) one by one. Since the inner for loop iterates
# overs a fixed number of bytes it does not change the time complexity.
def tokenize(text: str) -> list:
	''' reads in a text and returns a list of the tokens in that string '''
	tokensList = []
	token = ""
	for ch in text + " ":
		if isAlphaNum(ch):
			token += ch
		else:
			if token != "":
				tokensList.append(token.lower())
				token = "" 
	return tokensList


# Time complexity of this method is linear  O(n) if n is the
# number  of tokens in the list. The method iterates through 
# the tokens  one by one in one for loop
def computeWordFrequencies(tokensList: list) -> dict:
	''' counts the number of occurrences of each
	token in the token list and returns them in a dictionary '''
	d = {}
	for word in tokensList:
		if not word in d.keys():
			d[word] = 1
		else:
			d[word]+= 1
	return d


# Time complexity of this method is log-linear  O(n log n). The sorted() 
# method has a complexity of O(n log n) and the for loop has a time
# time complexity of O(n). Therefore the time complexity of thr whole
# method is the higher order term which is n log n
def printFrequencies(frequencies: dict) -> None:
	''' prints out the word frequency count'''
	sortedTuple = sorted(frequencies.items(), key= lambda x:x[1], reverse = True)
	for key, value in sortedTuple:
		print(str(key) + " = " + str(value))