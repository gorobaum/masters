import math
import numpy
from pylab import *
from numpy import ma

def bilinear(imagePixels, x, y, width, height):
	u = math.trunc(x)
	v = math.trunc(y)
	pixelOne = getPixel(imagePixels, width, height, u, v)
	pixelTwo = getPixel(imagePixels, width, height, u+1, v)
	pixelThree = getPixel(imagePixels, width, height, u, v+1)
	pixelFour = getPixel(imagePixels, width, height, u+1, v+1)

	interpolation = (u+1-x)*(v+1-y)*pixelOne*1.0 + (x-u)*(v+1-y)*pixelTwo*1.0 + (u+1-x)*(y-v)*pixelThree*1.0 + (x-u)*(y-v)*pixelFour*1.0
	return interpolation

def nearestNeighbor(imagePixels, x, y, width, height):
	realX = getNearestInteger(x)
	realY = getNearestInteger(y)
	return	getPixel(imagePixels, width, height, realX, realY)

def getPixel(pixels, width, height, x, y):
	# print width, height, x, y
	if x > width-1 or x < 0:
		return 0.0
	elif y > height-1 or y < 0:
		return 0.0
	else:
		return pixels[y, x]

def getNearestInteger(number):
	if number - math.floor(number) <= 0.5:
		return math.floor(number)
	else :
		return math.floor(number) + 1.0