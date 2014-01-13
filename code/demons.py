from PIL import Image

def demons(moving, static):
	deformed = Image.new(moving.mode, moving.size)
	deltaV = list(static.getdata())
	SIpixels = list(static.getdata())
	MIpixels = list(moving.getdata())
	listV = list()

	# for iteration in range(100):
	# 	deformedPixels = deformed.load()
	# 	movingPixels = moving.load()
	# 	w, h = deformed.size
	# 	for x in range(w):
	# 		for y in range(h):
	# 			deformedPixels[x, y] = 

