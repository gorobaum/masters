import time
import aux
import numpy
import scipy
from scipy import ndimage
from PIL import Image

def demon(staticPixels, movingPixels):
	# Compute Gradient Vector for the static image
	gradients = findGrad(staticPixels)
	# Get the pixels for the static, moving and deformed image
	deformedPixels = numpy.ndarray(staticPixels.shape, dtype=int)
	# Create the displacement field
	height, width = deformedPixels.shape
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
				deformedPixels[y, x] = aux.bilinearInterpolation(movingPixels, mix, miy, width, height)
				# update displvector
				updateDisplVector(displField, gradients, deformedPixels, staticPixels, i, x ,y)
		displField = ndimage.filters.gaussian_filter(displField, 1)
		total_time = total_time + time.time() - loop_time
		print "iteration ", iteration, "took ", time.time() - loop_time, "seconds."
		imageName = "result" + str(iteration) + ".jpg"
		scipy.misc.imsave(imageName, deformedPixels)
	print "Total execution time", total_time

def updateDisplVector(displField, gradients, deformedPixels, staticPixels, i, x ,y):
	dif = (deformedPixels[y, x] - staticPixels[y, x])
	div = pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow(dif, 2)
	if div != 0:
		newDisplX = dif*gradients[i][0]*1.0/div
		if abs(newDisplX) > 0.001:
			displField[i][0] = displField[i][0] + newDisplX
		newDisplY = dif*gradients[i][1]*1.0/div
		if abs(newDisplY) > 0.001:
			displField[i][1] = displField[i][1] + newDisplY

def findGrad(imagePixels):
	dx = ndimage.sobel(imagePixels, 0) # horizontal derivative
	dy = ndimage.sobel(imagePixels, 1) # vertical derivative
	gradX = dx.flatten().tolist()
	gradY = dy.flatten().tolist()
	grad = zip(gradX, gradY)
	return grad

def createDisplField(w, h):
	displField = list()
	for x in range(w):
		for y in range(h):
			displField.append([0.0,0.0])
	return displField