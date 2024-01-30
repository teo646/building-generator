from maskCanvas import canvas, point, showImage
from buildingGenerator import villa
from math import pi

def main():
    c = canvas()
    v = villa(point(100,100), pi/4, pi/6, 7, 5, 3, scale=1)
    lines = v.getRoof()
    for i in range(len(lines)):
        c.registerLineSeg(lines[i])

    showImage(c.draw(10))

if __name__ == "__main__":
    main()

