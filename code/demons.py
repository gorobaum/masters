import ImageFilter
import time
import aux
import numpy
import scipy
from scipy import ndimage
from PIL import Image

def demons(movingImage, staticImage):
	gradients = findGrad(staticImage)
	staticPixels = staticImage.load()
	movingPixels = movingImage.load()
	deformedImage = Image.new(movingImage.mode, movingImage.size)
	deformedPixels = deformedImage.load()
	
	width, height = deformedImage.size
	displVectors = createDisplVectors(width, height)
	iteration = 0
	start_time = time.time()
	for a in range(100):
		loop_time = time.time()
		print 'Iteration number ' + str(iteration)
		for y in range(height):
			for x in range(width):
				i = y*width+x
				# update deformed image
				mix = x-displVectors[i][0]
				miy = y-displVectors[i][1]
				deformedPixels[x, y] = aux.bilinearInterpolation(movingPixels, mix, miy, width, height)
				# update displvector
				updateDisplVector(displVectors, gradients, deformedPixels, staticPixels, i, x ,y)
		displVectors = ndimage.filters.gaussian_filter(displVectors, 1)
		print "iteration ", iteration, "took ", time.time() - loop_time, "seconds."
		imageName = "result" + str(iteration) + ".jpg"
		iteration += 1
		deformedImage.save(imageName)

def updateDisplVector(displVectors, gradients, deformedPixels, staticPixels, i, x ,y):
	dif = (deformedPixels[x, y] - staticPixels[x, y])
	div = (pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow(dif, 2))
	if div == 0: div = 1e-3
	newDisplX = dif*gradients[i][0]/div
	if abs(newDisplX) > 1e-5:
		displVectors[i][0] = displVectors[i][0] + newDisplX
	newDisplY = dif*gradients[i][1]/div
	if abs(newDisplY) > 1e-5:
		displVectors[i][1] = displVectors[i][1] + newDisplY

def findGrad(image):
	im = scipy.misc.imread('teste.jpg')
	im = im.astype('int32')
	dx = ndimage.sobel(im, 0) # horizontal derivative
	dy = ndimage.sobel(im, 1) # vertical derivative
	mag = numpy.hypot(dx, dy) # magnitude
	mag *= 255.0 / numpy.max(mag) # normalize (Q&D)
	scipy.misc.imsave('sobel.jpg', mag)
	return list()

def createDisplVectors(w, h):
	displVectors = list()
	for x in range(w):
		for y in range(h):
			displVectors.append([0,0])
	return displVectors
