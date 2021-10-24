import numpy 
import numpy as np
from PIL import Image 
import matplotlib.image as img
from scipy.ndimage import rotate

import functools
from typing import Any, Tuple

def rotate45_square(T):
	"""
		This rotate function is only used for square matrix 
	"""
	direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]

	# res = [[T[0][0] for i in range(len(T))] for i in range(len(T))]
	res = numpy.copy(T)
	for t in range(0, int( (len(T)+1)/2 )):
		x = t
		y = t

		L_x = t 
		R_x = len(T) - t - 1

		L_y = t 
		R_y = len(T) - t - 1

		cur = 0
		while 1:
			if x + direction[cur][0] > R_x or x + direction[cur][0] < L_x: 
				cur = (cur + 1) % 4 
			if y + direction[cur][1] < L_y or y + direction[cur][1] > R_y:
				cur = (cur + 1) % 4 

			u = x + direction[cur][0] 
			v = y + direction[cur][1]
			if u < L_x or u > R_x or v < L_y or v > R_y:
				res[x][y] = T[x][y]
				break

			res[u][v] = T[x][y]

			x = u 
			y = v
			if x == t and y == t:
				break
	return res
 
def read_image(path):
	image = Image.open(path)
	imgGray = image.convert('L')

	data = numpy.asarray(imgGray)
	return data 

def convolve(I, T):
	res = numpy.zeros(I.shape)

	for i in range(1, len(I)-1):
		for j in range(1, len(I[i])-1):
			print(j)

			# res[i][j] = 0
			for r in range(len(T)):
				for c in range(len(T[r])):
					res[i][j] += I[i+r-1][j+c-1] * T[r][c]
	return res

if __name__ == "__main__":
	# read image 
	path = "bear.png"
	grayMatrix = read_image(path)

	# add padding 
	I = numpy.pad(grayMatrix, 1, mode='edge')

	# Robinson bac3 window 
	T = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]

	# rotate 
	resMatrix = numpy.zeros(grayMatrix.shape)
	for i in range(8):
		H = convolve(I, T)

		# update resMatrix
		for i in range(len(grayMatrix)):
			for j in range(len(grayMatrix[i])):
				resMatrix[i][j] = max( resMatrix[i][j], abs(H[i+1][j+1]) )

		T = rotate45_square(T)

	# export image
	resImage = Image.fromarray(resMatrix)
	resImage = resImage.convert("L")
	resImage.save("resuslt.png")
	resImage.show()

