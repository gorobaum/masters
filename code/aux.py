import math
import numpy
import interpolation
import matplotlib.pyplot as plt
from pylab import *

def sumOfField(ndarray):
	result = 0.0
	for y in range(ndarray.shape[0]):
		for x in range(ndarray.shape[1]):
			result = result + abs(ndarray[y][x][0]) + abs(ndarray[y][x][1])
	return result

def deformSin(imagePixels):
	deformedPixels = numpy.ndarray(imagePixels.shape, dtype=int32)
	h, w = imagePixels.shape
	for i in range(h):
		for j in range(w):
			newY = i + math.sin(j/16)
			newX = j 
			deformedPixels[i,j] = interpolation.bilinear(imagePixels, newX, newY, w, h)
	return deformedPixels

def saveVectorField(width, height, xVec, yVec, imageName):
	x = linspace(0, width, width+1)
	y = linspace(0, height, height+1)
	X,Y = meshgrid(x, y)
	figure()
	Q = quiver(X, Y, xVec, yVec)

	title(imageName)
	savefig(imageName+".jpg")
