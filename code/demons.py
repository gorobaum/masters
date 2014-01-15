from PIL import Image
import ImageFilter
import Scipy

def demons(movingImage, staticImage):
	gradients = findGrad(staticImage)

	staticPixels = staticImage.load()
	movingPixels = movingImage.load()
	deformedImage = Image.new(movingImage.mode, movingImage.size)
	deformedPixels = deformedImage.load()
	
	width, height = deformedImage.size
	displVectors = createDisplVectors(width, height)

	for x in range(width):
		for y in range(height):
			i = x*height+y
			# update deformed image
			mix = max(0, min(x-displVectors[i][0], width))
			miy = max(0, min(y-displVectors[i][1], height))
			deformedPixels[x, y] = movingPixels[mix, miy]
			# update displacement vector
			divx = (pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow((deformedPixels[x, y] - staticPixels[x, y]), 2))
			divy = (pow(gradients[i][0], 2) + pow(gradients[i][1], 2) + pow((deformedPixels[x, y] - staticPixels[x, y]), 2))
			if divx == 0:
				displVectors[i][0] = 0
			else: 
				displVectors[i][0] = displVectors[i][0] + (deformedPixels[x, y] - staticPixels[x, y])*gradients[i][0]/divx
			if divy == 0:
				displVectors[i][1] = 0
			else:
				displVectors[i][1] = displVectors[i][1] + (deformedPixels[x, y] - staticPixels[x, y])*gradients[i][1]/divy
	displVectors = scipy.ndimage.filters.gaussian_filter(displVectors, 1)



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