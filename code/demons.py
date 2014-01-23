import ImageFilter
import time
import aux
import numpy
import scipy
from scipy import ndimage
from PIL import Image

def demons(movingImage, staticImage):
	# Compute Gradient Vector for the static image
	gradients = findGrad(staticImage)
	# Get the pixels for the static, moving and deformed image
	staticPixels = staticImage.load()
	movingPixels = movingImage.load()
	deformedImage = Image.new(staticImage.mode, staticImage.size, "black")
	deformedPixels = deformedImage.load()
	# Create the displacement field
	width, height = deformedImage.size
	displField = createDisplField(width, height)
	total_time = 0
	for iteration in range(100):
		loop_time = time.time()
		print 'Iteration number ' + str(iteration)
		for y in range(height):
			for x in range(width): 
				i = y*width+x
				# update deformed image
				mix = x-displField[i][0]
				miy = y-displField[i][1]
				deformedPixels[x, y] = aux.bilinearInterpolation(movingPixels, mix, miy, width, height)
				# update displvector
				updateDisplVector(displField, gradients, deformedPixels, staticPixels, i, x ,y)
		displField = ndimage.filters.gaussian_filter(displField, 1)
		total_time = total_time + time.time() - loop_time
		print "iteration ", iteration, "took ", time.time() - loop_time, "seconds."
		imageName = "result" + str(iteration) + ".jpg"
		deformedImage.save(imageName)
	print "Total execution time", total_time

def updateDisplVector(displField, gradients, deformedPixels, staticPixels, i, x ,y):
	dif = (deformedPixels[x, y] - staticPixels[x, y])
	div = pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow(dif, 2)
	if div != 0:
		newDisplX = dif*gradients[i][0]*1.0/div
		if abs(newDisplX) > 1e-5:
			displField[i][0] = displField[i][0] + newDisplX
		newDisplY = dif*gradients[i][1]*1.0/div
		if abs(newDisplY) > 1e-5:
			displField[i][1] = displField[i][1] + newDisplY

def findGrad(image):
	im = scipy.misc.fromimage(image)
	im = im.astype('int32')
	dx = ndimage.sobel(im, 0) # horizontal derivative
	dy = ndimage.sobel(im, 1) # vertical derivative
	sobelX = scipy.misc.toimage(dx)
	sobelY = scipy.misc.toimage(dy)
	gradX = list(sobelX.getdata())
	gradY = list(sobelY.getdata())
	grad = zip(gradX, gradY)
	return grad

def createDisplField(w, h):
	displField = list()
	for x in range(w):
		for y in range(h):
			displField.append([0,0])
	return displField

