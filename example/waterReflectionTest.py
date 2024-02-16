from maskCanvas import canvas, point, showImage, line_seg
from buildingGenerator import angled_roof_left as left
from buildingGenerator import angled_roof_right as right
from buildingGenerator import angled_roof_integrated as integrated
from math import pi
import cv2
import numpy as np
def main():
    c = canvas()
    
    L = integrated(point(200, 200), pi/4, pi/6, 7, 3, 5, scale=2)
    c = L.draw(c)

    image = np.flip(c.draw(4), axis=0)
    cv2.imwrite("./angled_roof.jpg", image)
    showImage(image)



if __name__ == "__main__":
    main()

