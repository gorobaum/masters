from PIL import Image

try:
	original = Image.open("../testImages/msc.jpg")
except:
	print "Unabel to load image!"

print "The size of the image is:"
print(original.format, original.size, original.mode)