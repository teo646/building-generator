from maskCanvas import canvas, point, showImage, line_seg
from buildingGenerator import straight_roof_left as left
from buildingGenerator import straight_roof_right as right
from buildingGenerator import straight_roof_integrated as integrated
from math import pi
import cv2

def main():
    c = canvas()

    L = left(point(30,210), pi/4, 0, 7, 3, 5, scale=2)
    c = L.draw(c)

    L = left(point(345,210), pi/4, pi/2, 7, 3, 5, scale=2)
    c = L.draw(c)

    L = left(point(510,210), pi/4, pi/3, 7, 3, 5, scale=2)
    c = L.draw(c)
    
    c.registerLineSeg(line_seg([[0,215], [600, 215]], (80,80,80), 5))
    
    R = right(point(30,420), pi/4, 0, 7, 3, 5, scale=2)
    c = R.draw(c)

    R = right(point(345,420), pi/4, pi/2, 7, 3, 5, scale=2)
    c = R.draw(c)

    R = right(point(510,420), pi/4, pi/3, 7, 3, 5, scale=2)
    c = R.draw(c)

    c.registerLineSeg(line_seg([[0,425], [600, 425]], (80,80,80), 5))

    I = integrated(point(30,625), pi/4, 0, 7, 3, 5, scale=2)
    c = I.draw(c)

    I = integrated(point(345,625), pi/4, pi/2, 7, 3, 5, scale=2)
    c = I.draw(c)

    I = integrated(point(510,625), pi/4, pi/3, 7, 3, 5, scale=2)
    c = I.draw(c)

    image = c.draw(10)
    cv2.imwrite("./straight_roof.jpg", image)
    showImage(image)



if __name__ == "__main__":
    main()

