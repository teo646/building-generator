from maskCanvas import canvas, point, showImage, line_seg
from buildingGenerator import angled_roof_left as left
from buildingGenerator import angled_roof_right as right
from buildingGenerator import angled_roof_integrated as integrated
from math import pi
import cv2
import numpy as np
def main():
    c = canvas()
    
    for i in range(0,5):
        for j in range(0,5):
            L = integrated(point(110+110*i, 105+105*j), pi/8*i, pi/8*j, 7, 3, 5, scale=1)
            c = L.draw(c)

    image = c.draw(20)
    cv2.imwrite("./angled_roof.jpg", image)
    showImage(image)



if __name__ == "__main__":
    main()

