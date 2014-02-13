import sys
import aux
import scipy
import demons
from scipy import ndimage

if len(sys.argv) <= 2:
	print "Please pass the image name as an arg"
	sys.exit()
else:
	try:
		original = scipy.misc.imread(sys.argv[1], False)
		modified = scipy.misc.imread(sys.argv[2], False)
	except:
		print "Unable to load image!"

	demons.demon(original,modified)
