from gp import Render

width, height = 800, 600

White = (255, 255, 255)
r = Render(width, height)

a = [(165, 380), (185, 360), (185, 360), (180, 330), (180, 330), (207, 345), (207, 345), (233, 330), (233, 330), (230, 360),
     (230, 360), (250, 380), (250, 380), (220, 385), (220, 385), (205, 410), (205, 410), (193, 383), (193, 383), (165, 380)]


def drawPoligon(array):
    for i in range(len(array)):
        print(i)
        if i + 1 < len(array):
            r.line(array[i], array[i + 1])
        if i + 1 > len(array):
            r.line(array[i + 1], array[0])


def minmax(array):
	ys = []
	xs = []
	for i in array:
		xs.append(i[0])
		ys.append(i[1])

	print(min(ys),max(ys),min(xs), max(xs))


#drawPoligon(a)

#r.write('lab5.bmp')

minmax(a)
