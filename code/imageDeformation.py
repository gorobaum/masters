import sys
import aux
import scipy
from scipy import ndimage

if len(sys.argv) <= 1:
	print "Please pass the image name as an arg"
	sys.exit()
else:
	try:
		original = scipy.misc.imread(sys.argv[1], True)
	except:
		print "Unable to load image!"

	modified = aux.deformSin(original)
	scipy.misc.imsave("../testImages/modified-teste.jpg", modified)
	print "Transformation sucessful with the name modified-teste.jpg"