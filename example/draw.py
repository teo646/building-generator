from maskCanvas import canvas, point, showImage
from buildingGenerator import villa
from math import pi

def main():
    c = canvas()
    v = villa(point(230,350), 0, pi/2, 7, 3, 5, scale=2)
    c = v.draw(c)


    v = villa(point(170,200), pi/4, pi/3, 7, 3, 5, scale=2)
    c = v.draw(c)

    v = villa(point(30,350), 0, 0, 7, 3, 5, scale=2)
    c = v.draw(c)

    showImage(c.draw(10))


if __name__ == "__main__":
    main()

