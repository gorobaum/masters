import sys
import aux
import scipy
import demons
from scipy import ndimage

if len(sys.argv) <= 2:
	print "Please use as <Original Image> and <Modified Image>"
	sys.exit()
else:
	try:
		original = scipy.misc.imread(sys.argv[1], True)
		modified = scipy.misc.imread(sys.argv[2], True)
	except:
		print "Unable to load image!"

	demons.demon(original,modified)
