from PIL import Image
import ImageFilter
import scipy.ndimage as ndimage
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
	for a in range(100):
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
				updateDisplVector(displVectors, gradients, deformedPixels, staticPixels, i, x ,y)
		displVectors = ndimage.filters.gaussian_filter(displVectors, 1)
		print "iteration ", iteration, "took ", time.time() - loop_time, "seconds."
		imageName = "result" + str(iteration) + ".jpg"
		iteration += 1
		deformedImage.save(imageName)

def updateDisplVector(displVectors, gradients, deformedPixels, staticPixels, i, x ,y):
	div = (pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow((deformedPixels[x, y] - staticPixels[x, y]), 2))
	if div == 0: div = 1e-3
	vAdd = (deformedPixels[x, y] - staticPixels[x, y])/div
	newDisplX = vAdd*gradients[i][0]
	if abs(newDisplX) > 1e-5:
		displVectors[i][0] = displVectors[i][0] + newDisplX
	newDisplY = vAdd*gradients[i][1]
	if abs(newDisplY) > 1e-5:
		displVectors[i][1] = displVectors[i][1] + newDisplY

def findGrad(image):
	dx = ImageFilter.Kernel((3, 3), (1,0,-1,2,0,-2,1,0,-1), 8, offset=0)
	dy = ImageFilter.Kernel((3, 3), (-1,-2,-1,0,0,0,1,2,1), 8, offset=0)
	xImage = image.filter(dx)
	yImage = image.filter(dy)
	gradX = list(xImage.getdata())
	gradY = list(yImage.getdata())
	grad = zip(gradX, gradY)
	return grad

def createDisplVectors(w, h):
	displVectors = list()
	for x in range(w):
		for y in range(h):
			displVectors.append([0,0])
	return displVectors
