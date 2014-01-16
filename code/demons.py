from PIL import Image
import ImageFilter
import scipy.ndimage as ndimage
import time

def demons(movingImage, staticImage):
	gradients = findGrad(staticImage)
	staticPixels = staticImage.load()
	movingPixels = movingImage.load()
	deformedImage = Image.new(movingImage.mode, movingImage.size)
	deformedPixels = deformedImage.load()
	
	width, height = deformedImage.size
	displVectors = createDisplVectors(width, height)
	cont = True
	iteration = 0
	start_time = time.time()
	while cont:
		loop_time = time.time()
		cont = False
		print 'Iteration number ' + str(iteration)
		for x in range(width):
			for y in range(height):
				i = x*height+y
				# update deformed image
				mix = round(max(0, min(x-displVectors[i][0], width)))
				miy = round(max(0, min(y-displVectors[i][1], height)))
				deformedPixels[x, y] = movingPixels[mix, miy]
				# update displacement vector x
				divx = (pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow((deformedPixels[x, y] - staticPixels[x, y]), 2))
				if divx == 0:
					displVectors[i][0] = 0
				else: 
					newDisplX = displVectors[i][0] + (deformedPixels[x, y] - staticPixels[x, y])*gradients[i][0]/divx
					if not cont and (round(displVectors[i][0] - newDisplX) != 0):
						cont = True
						displVectors[i][0] = displVectors[i][0] + newDisplX
				# update displacement vector y
				divy = (pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow((deformedPixels[x, y] - staticPixels[x, y]), 2))
				if divy == 0:
					displVectors[i][1] = 0
				else:
					newDisplY = displVectors[i][1] + (deformedPixels[x, y] - staticPixels[x, y])*gradients[i][1]/divy
					if not cont and (round(displVectors[i][1] - newDisplY) != 0):
						cont = True
						displVectors[i][1] = displVectors[i][1] + newDisplY
		displVectors = ndimage.filters.gaussian_filter(displVectors, 1)
		print "iteration ", iteration, "took ", time.time() - loop_time, "seconds."
		deformedImage.show()	
		iteration += 1
	deformedImage.show()
	imageName = "result" + str(iteration) + ".jpg"
	deformedImage.save(imageName)



def findGrad(image):
	dx = ImageFilter.Kernel((3, 3), (-1,0,1,-1,0,1,-1,0,1), scale=None, offset=0)
	dy = ImageFilter.Kernel((3, 3), (-1,-1,-1,0,0,0,1,1,1), scale=None, offset=0)
	xImage = image.filter(dx)
	yImage = image.filter(dy)
	gradX = list(xImage.getdata())
	gradY = list(xImage.getdata())
	grad = zip(gradX, gradY)
	return grad

def createDisplVectors(w, h):
	displVectors = list()
	for x in range(w):
		for y in range(h):
			displVectors.append([0,0])
	return displVectors
