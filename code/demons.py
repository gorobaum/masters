from PIL import Image
import ImageFilter
import scipy.ndimage
import time
import aux

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
	cont = True
	while cont:
		cont = False
		loop_time = time.time()
		print 'Iteration number ' + str(iteration)
		for x in range(width):
			for y in range(height):
				i = x*height+y
				# update deformed image
				mix = x-displVectors[i][0]
				miy = y-displVectors[i][1]
				deformedPixels[x, y] = aux.bilinearInterpolation(movingPixels, mix, miy, width, height)
				# update displvector
				if updateDisplVector(displVectors, gradients, deformedPixels, staticPixels, i, x ,y):
					cont = True
		displVectors = ndimage.filters.gaussian_filter(displVectors, 1)
		print "iteration ", iteration, "took ", time.time() - loop_time, "seconds."
		imageName = "result" + str(iteration) + ".jpg"
		iteration += 1
		deformedImage.save(imageName)

def updateDisplVector(displVectors, gradients, deformedPixels, staticPixels, i, x ,y):
	cont = False
	div = (pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow((deformedPixels[x, y] - staticPixels[x, y]), 2))
	if div == 0: div = 1e-3
	newDisplX = displVectors[i][0] + (deformedPixels[x, y] - staticPixels[x, y])*gradients[i][0]/div
	if newDisplX > 1e-5:
		displVectors[i][0] = displVectors[i][0] + newDisplX
		cont = True
	newDisplY = displVectors[i][1] + (deformedPixels[x, y] - staticPixels[x, y])*gradients[i][1]/div
	if newDisplY > 1e-5:
		displVectors[i][1] = displVectors[i][1] + newDisplY
		cont = True
	return cont

def findGrad(image):
	dx = ImageFilter.Kernel((3, 3), (1,0,-1,2,0,-2,1,0,-1), 8, offset=0)
	dy = ImageFilter.Kernel((3, 3), (-1,-2,-1,0,0,0,1,2,1), 8, offset=0)
	xImage = image.filter(dx)
	yImage = image.filter(dy)
	gradX = list(xImage.getdata())
	gradY = list(yImage.getdata())
	width, height = image.size
	aux.showVectorField(width, height, gradX, gradY)
	grad = zip(gradX, gradY)
	return grad

def createDisplVectors(w, h):
	displVectors = list()
	for x in range(w):
		for y in range(h):
			displVectors.append([0,0])
	return displVectors
