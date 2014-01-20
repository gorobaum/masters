from PIL import Image
import math

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
	if x >= width-1 or x <= 0:
		return 0.0
	elif y >= height-1 or y <= 0:
		return 0.0
	else:
		return pixels[x, y]