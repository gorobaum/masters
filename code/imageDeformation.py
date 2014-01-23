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
	except:
		print "Unable to load image!"

	modified = aux.deformSin(original)
	modified.save("../testImages/"+sys.argv[1]+"-m.jpg", "JPEG")
	print "The size of the original image is:"
	print(original.format, original.size, original.mode)

	print "The size of the modified image is:"
	print(modified.format, modified.size, modified.mode)


	Demons.demons(modified, original)