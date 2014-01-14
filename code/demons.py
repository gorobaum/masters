from PIL import Image

def demons(movingImage, staticImage):
	deformedImage = Image.new(movingImage.mode, movingImage.size)
	listIntGradVector = findGrad(staticImage)
	SIpixels = list(staticImage.getdata())
	MIpixels = list(movingImage.getdata())
	listDisplVector = list()

	for iteration in range(100):
		deformedPixels = deformedImage.load()
		movingPixels = movingImage.load()
		w, h = deformedImage.size
		for x in range(w):
			for y in range(h):
				deformedPixels[x, y] = 

def findGrad(image):
	gradImage = image.filter(ImageFilter.FIND_EDGES)
	return list(image.getdata())