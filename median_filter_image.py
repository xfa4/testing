import numpy 
import numpy as np
from PIL import Image 
import matplotlib.image as img
from scipy.ndimage import rotate

import functools
from typing import Any, Tuple

def get_median_filter_matrix(I):
	res = numpy.zeros(I.shape)

	for i in range(1, len(I)-1):
		for j in range(1, len(I[i])-1):
			ls = []
			for r in range(0, 3):
				for c in range(0, 3):
					ls.append(I[i+r-1][j+c-1])
			ls.sort()

			res[i][j] = ls[int((len(ls)-1)/2)]
	return res

if __name__ == "__main__":
	# input matrix 
	I = [[5, 2, 7, 2, 6, 3], [3, 2, 8, 3, 5, 2], [7, 8, 2, 4, 7, 3], [4, 2, 6, 2, 5, 2]]

	# add padding 
	I = numpy.pad(I, 1, mode='edge')

	res = get_median_filter_matrix(I)

	for i in range(1, len(I)-1):
		for j in range(1, len(I[i])-1):
			print(int(res[i][j]), end=" ")
		print("")
