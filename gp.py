import struct

White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Green = (0, 255, 0)
Dark_Green = (0, 127, 0)
Sky_Blue = (15, 187, 196)
Yellow = (214, 232, 16)
Orange = (232, 149, 16)
Purple = (138, 16, 232)
Pink = (232, 16, 188)
Black = (0, 0, 0)


def char(c):
  return struct.pack('=c', c.encode('ascii'))


def word(w):
  return struct.pack('=h', w)


def dword(d):
  return struct.pack('=l', d)


def color(x):
  b = x[2]
  g = x[1]
  r = x[0]
  return bytes([b, g, r])


class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.pixels = []
    self.clear()

  def clear(self):
    self.pixels = [[color(Black) for x in range(self.width)]
                   for y in range(self.height)]

  def point(self, x, y, color):
    self.pixels[x][y] = color

  def line(self, start, end, colors=White):
    x1, y1 = start
    x2, y2 = end
    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
    steep = dy > dx

    if steep:
      x1, y1 = y1, x1
      x2, y2 = y2, x2
    if x1 > x2:
      x1, x2 = x2, x1
      y1, y2 = y2, y1
    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx
    y = y1

    for x in range(x1, x2 + 1):
      if steep:
        self.point(y, x, color(colors))
      else:
        self.point(x, y, color(colors))

      offset += dy * 2
      if offset >= threshold:
        y += 1 if y1 < y2 else -1
        threshold += 2 * dx

  def write(self, filename):
    f = open(filename, 'wb')

    # file header
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    for x in range(self.height):
      for y in range(self.width):
        f.write(self.pixels[x][y])

    f.close()

  def load(self, filename, translate=(0, 0), scale=(1, 1)):

    model = Obj(filename)

    for face in model.vfaces:
      vcount = len(face)
      for j in range(vcount):
        f1 = face[j][0]
        f2 = face[(j + 1) % vcount][0]

        v1 = model.vertices[f1 - 1]
        v2 = model.vertices[f2 - 1]

        scaleX, scaleY = scale
        translateX, translateY = translate

        x1 = round((v1[0] + translateX) * scaleX)
        y1 = round((v1[1] + translateY) * scaleY)
        x2 = round((v2[0] + translateX) * scaleX)
        y2 = round((v2[1] + translateY) * scaleY)

    self.line((x1, y1), (x2, y2), White)


class Obj(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.lines = f.read().splitlines()
      self.vertices = []
      self.vfaces = []
      self.read()

  def read(self):
    for line in self.lines:
      if line:
        prefix, value = line.split(' ', 1)
        if prefix == 'v':
          self.vertices.append(list(map(float, value.split(' '))))
        elif prefix == 'f':
          self.vfaces.append([list(map(int, face.split('/')))
                              for face in value.split(' ')])


#r = Render(800, 600)
#r.line((10, 10), (200, 100), Pink)
#r.line((10, 10), (500, 660), Green)
#r.line((10, 10), (400, 200), Sky_Blue)
#r.point(200, 200, color(White))
# r.write('out2.bmp')
