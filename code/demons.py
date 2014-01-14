from PIL import Image
import ImageFilter

def demons(movingImage, staticImage):
	intGradVectors = findGrad(staticImage)

	staticPixels = staticImage.load()
	movingPixels = movingImage.load()
	deformedImage = Image.new(movingImage.mode, movingImage.size)
	deformedPixels = deformedImage.load()
	
	width, height = deformedImage.size
	displVectors = createDisplVectors(width, height)

	print (deformedPixels[0, 0] - staticPixels[0, 0])*intGradVectors[0, 0]/((pow(intGradVectors[0, 0], 2)) + pow((deformedPixels[0, 0] - staticPixels[0, 0]), 2))

	# for iteration in range(100):
	# for x in range(width):
	# 	for y in range(height):
	# 		i = x*height+y
	# 		mix = max(0, min(x-displVectors[i][0], width))
	# 		miy = max(0, min(y-displVectors[i][1], height))
	# 		deformedPixels[x, y] = movingPixels[mix, miy]
	# print "termino de updeita"
	# for x in range(width):
	# 	for y in range(height):
	# 		i = x*height+y
	# 		displVectors[i] += (deformedPixels[x, y] - staticPixels[x, y])*intGradVectors[x, y]/((pow(intGradVectors[x, y], 2)) + pow((deformedPixels[x, y] - staticPixels[x, y]), 2))



def findGrad(image):
	sobelFilterX = ImageFilter.Kernel((3, 3), (1,0,-1,2,0,-2,1,0,-1), scale=None, offset=0)
	sobelFilterY = ImageFilter.Kernel((3, 3), (1,2,1,0,0,0,-1,-2,-1), scale=None, offset=0)
	gradImage = image.filter(sobelFilterX)
	gradImage = gradImage.filter(sobelFilterY)
	return gradImage.load()

def createDisplVectors(w, h):
	displVectors = list()
	for x in range(w):
		for y in range(h):
			displVectors.append((0,0))
	return displVectors