import math
import numpy
from pylab import *
from numpy import ma

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
			newY = i + math.sin(j/8)
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

def saveVectorField(width, height, xVec, yVec, imageName):
	x = linspace(-1*width/2, width/2, width)
	y = linspace(-1*height/2, height/2, height)
	X,Y = meshgrid(x, y)
	figure()
	Q = quiver(X, Y, xVec, yVec)
	qk = quiverkey(Q, 1, 1.05, 0.5, '')
	l,r,b,t = axis()
	dx, dy = r-l, t-b
	axis([l-0.05*dx, r+0.05*dx, b-0.05*dy, t+0.05*dy])

	title(imageName)
	savefig(imageName+".jpg")
