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
	currentDisplacement = createDisplField(width, height)
	total_time = 0.0
	iteration = 1
	stop = False
	norm = numpy.ndarray(10, dtype=float)
	norm.fill(0.0)
	while not stop:
		loop_time = time.time()
		print 'Iteration number ' + str(iteration)
		for y in range(height):
			for x in range(width):
				# update deformed image
				mix = x-displField[y][x][0]
				miy = y-displField[y][x][1]
				deformedPixels[y, x] = aux.bilinearInterpolation(movingPixels, mix, miy, width, height)
				# update displvector
				updateCurrentDisplacement(currentDisplacement, gradients, deformedPixels, staticPixels, x ,y)
		displField = updateDisplFiled(displField, currentDisplacement)
		plotField(iteration, displField)
		total_time = total_time + time.time() - loop_time
		imageName = "result" + str(iteration) + ".jpg"
		scipy.misc.imsave(imageName, deformedPixels)
		print "iteration ", iteration, "took ", time.time() - loop_time, "seconds."
		stop = stopCriteria(norm, displField, currentDisplacement)
		iteration = iteration + 1
	print "Total execution time", total_time

def stopCriteria(norm, displField, currentDisplacement):
	newNorm = aux.sumOfField(displField)/aux.sumOfField(currentDisplacement)
	if (newNorm - norm[9]) <= 1e-4:
		return True
	else:
		for i in range(9):
			norm[i+1] = norm[i]
		norm[0] = newNorm
		return False

def plotField(iteration, displField):	
	fieldName = "VFI-" + str(iteration)
	height = displField.shape[0]
	width = displField.shape[1]
	xVec = list()
	yVec = list()
	for y in range(displField.shape[0]):
		for x in range(displField.shape[1]):
			xVec.append([displField[y][x][0],0])
			yVec.append([0,displField[y][x][1]])
	aux.saveVectorField(width, height, xVec, yVec, fieldName)

def updateDisplFiled(displField, currentDisplacement):
	displField = displField + currentDisplacement
	displField = ndimage.filters.gaussian_filter(displField, 1.0)
	return displField

def updateCurrentDisplacement(currentDisplacement, gradients, deformedPixels, staticPixels, x ,y):
	dif = (deformedPixels[y, x] - staticPixels[y, x])
	div = pow(gradients[y][x][0], 2) + pow(gradients[y][x][1], 2) + pow(dif, 2)
	if div != 0:
		currentDisplacement[y][x][0] = dif*gradients[y][x][0]*1.0/div
		currentDisplacement[y][x][1] = dif*gradients[y][x][1]*1.0/div
	else:
		currentDisplacement[y][x][0] = 0.0
		currentDisplacement[y][x][1] = 0.0

def findGrad(imagePixels):
	dx = ndimage.sobel(imagePixels, 0) # horizontal derivative
	dy = ndimage.sobel(imagePixels, 1) # vertical derivative
	# mag = numpy.hypot(dx, dy)  # magnitude
	# mag *= 255.0 / numpy.max(mag)  # normalize (Q&D)
	# scipy.misc.imshow(mag)
	grad = scipy.ndarray((dx.shape[0],dx.shape[1], 2), dtype=float)
	for y in range(dx.shape[0]):
		for x in range(dx.shape[1]):
			grad[y][x][0] = dx[y][x]
			grad[y][x][1] = dy[y][x]
	return grad

def createDisplField(width, height):
	aux = scipy.ndarray((height,width, 2), dtype=float)
	aux.fill(0.0)
	return aux
