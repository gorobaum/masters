from PIL import Image
import sys
import transformation as Transformations
import demons as Demons
import aux

if len(sys.argv) <= 1:
	print "Please pass the image name as an arg"
	sys.exit()
else:
	try:
		original = Image.open(sys.argv[1])
		original = original.convert("L") # Convert to greyscale
	except:
		print "Unable to load image!"

	modified = aux.deformSin(original)

	print "The size of the modified image is:"
	print(modified.format, modified.size, modified.mode)

	print "The size of the original image is:"
	print(original.format, original.size, original.mode)

	Demons.demons(modified, original)