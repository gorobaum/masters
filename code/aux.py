import math
import numpy
from pylab import *
from numpy import ma

def deformSin(imagePixels):
	deformedPixels = numpy.ndarray(imagePixels.shape, dtype=int)
	h, w = imagePixels.shape
	for i in range(h):
		for j in range(w):
			newY = i + 4*math.sin(j/16)
			newX = j 
			deformedPixels[i,j] = bilinearInterpolation(imagePixels, newX, newY, w, h)
	return deformedPixels

def bilinearInterpolation(imagePixels, x, y, width, height):
	u = math.trunc(x)
	v = math.trunc(y)
	pixelOne = getPixel(imagePixels, width, height, u, v)
	pixelTwo = getPixel(imagePixels, width, height, u+1, v)
	pixelThree = getPixel(imagePixels, width, height, u, v+1)
	pixelFour = getPixel(imagePixels, width, height, u+1, v+1)

	interpolation = (u+1-x)*(v+1-y)*pixelOne*1.0 + (x-u)*(v+1-y)*pixelTwo*1.0 + (u+1-x)*(y-v)*pixelThree*1.0 + (x-u)*(y-v)*pixelFour*1.0
	return interpolation

def getPixel(pixels, width, height, x, y):
	# print width, height, x, y
	if x > width-1 or x < 0:
		return 0.0
	elif y > height-1 or y < 0:
		return 0.0
	else:
		return pixels[y, x]

def showVectorField(width, height, xVec, yVec):
	X,Y = meshgrid(arange(width), arange(height))
	#1
	figure()
	Q = quiver(X, Y, xVec, yVec)
	qk = quiverkey(Q, 0.5, 1.05, 1, '')
	l,r,b,t = axis()
	dx, dy = r-l, t-b
	axis([l-0.05*dx, r+0.05*dx, b-0.05*dy, t+0.05*dy])

	title('teste')
	show()