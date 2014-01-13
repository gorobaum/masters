from PIL import Image

def affine(original, m ,n):
	width, height = original.size
	xshift = abs(m) * width
	yshift = abs(n) * height
	new_width = width + int(round(xshift))
	new_height = height + int(round(yshift))
	out = original.transform((new_width, new_height), Image.AFFINE, (1, m, -xshift if m > 0 else 0, n, 1, -yshift if n > 0 else 0), Image.BICUBIC)
	return out
