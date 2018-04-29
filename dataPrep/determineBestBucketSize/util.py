

def vectorIsEmpty(vector):
	empty = True
	for val in vector:
		empty = empty and (val == 0)

	return empty

def concatenateMatrix(matrix):
	concatenation = []
	for list_ in matrix:
		concatenation += list_

	return concatenation