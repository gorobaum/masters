from PIL import Image
import sys
import transformation as Transformations

print sys.argv[1]

try:
	original = Image.open(sys.argv[1])
except:
	print "Unabel to load image!"

print "The size of the original image is:"
print(original.format, original.size, original.mode)

modified = Transformations.affine(original, -0.5, 0)

print "The size of the modified image is:"
print(modified.format, modified.size, modified.mode)

modified.show()