from PIL import Image
import transformation as Transformations

try:
	original = Image.open("../testImages/msc.jpg")
except:
	print "Unabel to load image!"

print "The size of the image is:"
print(original.format, original.size, original.mode)
out = Transformations.affine(original, -0.1, 0.1)
out.show()