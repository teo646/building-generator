from maskCanvas import canvas, point, showImage
from buildingGenerator import standard, opposite_dir
from math import pi

def main():
    c = canvas()
    oppo = opposite_dir(point(300,300), pi/4, pi/6, 7, 3, 5, scale=2)
    stand = standard(point(300,300), pi/4, pi/6, 7, 3, 5, scale=2)
    c = oppo.draw(c)
    c = stand.draw(c)

    showImage(c.draw(10))


if __name__ == "__main__":
    main()

