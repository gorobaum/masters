import sys
import aux
import scipy
from scipy import ndimage

if len(sys.argv) <= 1:
	print "Please pass the image name as an arg and the type of interpolation"
	sys.exit()
else:
	try:
		original = scipy.misc.imread(sys.argv[1], True)
		typeOfInterpolation = sys.argv[2]
	except:
		print "Unable to load image!"

	aux.saveHistogram(original, "Original Image Histogram", "original-teste-h.jpg")
	modified = aux.deformSin(original, typeOfInterpolation)
	scipy.misc.imsave("../testImages/modified-teste.jpg", modified)
	aux.saveHistogram(modified, "Modified Image Histogram", "modified-teste-h"+typeOfInterpolation+".jpg")
	print "Transformation sucessful with the name modified-teste.jpg"