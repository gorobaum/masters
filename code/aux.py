from PIL import Image
import math
from pylab import *
from numpy import ma

def deformSin(image):
	deformedImage = Image.new(image.mode, image.size)
	imagePixels = image.load()
	deformedPixels = deformedImage.load()
	w, h = image.size
	for i in range(w):
		for j in range(h):
			newX = i + 4*math.sin(j/16)
			newY = j
			deformedPixels[i,j] = bilinearInterpolation(imagePixels, newX, newY, w, h)
	return deformedImage

def bilinearInterpolation(imagePixels, x, y, width, height):
	u = math.trunc(x)
	v = math.trunc(y)
	pixelOne = getPixel(imagePixels, width, height, u, v)
	pixelTwo = getPixel(imagePixels, width, height, u+1, v)
	pixelThree = getPixel(imagePixels, width, height, u, v+1)
	pixelFour = getPixel(imagePixels, width, height, u+1, v+1)

	interpolation = (u+1-x)*(v+1-y)*pixelOne + (x-u)*(v+1-y)*pixelTwo + (u+1-x)*(y-v)*pixelThree + (x-u)*(y-v)*pixelFour
	return interpolation

def getPixel(pixels, width, height, x, y):
	if x > width-1 or x < 0:
		return 0.0
	elif y > height-1 or y < 0:
		return 0.0
	else:
		return pixels[x, y]

def showVectorField(width, height, xVec, yVec, title):
	X,Y = meshgrid(arange(width), arange(height))
	#1
	figure()
	Q = quiver(X, Y, xVec, yVec)
	qk = quiverkey(Q, 0.5, 1.05, 1, '')
	l,r,b,t = axis()
	dx, dy = r-l, t-b
	axis([l-0.05*dx, r+0.05*dx, b-0.05*dy, t+0.05*dy])

	title(title)
	show()