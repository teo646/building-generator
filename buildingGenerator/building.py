from maskCanvas import lineSeg, canvas, point
from math import cos, sin

#
class building:
    
    def __init__(self, pitch, yaw, width_num, depth_num, height_num):
        self.yaw = yaw
        self.pitch = pitch
        self.width_num = width_num
        self.depth_num = depth_num
        self.height_num = height_num

    def getWidthPoint(self, point_, length):
        return point(point_.x - sin(self.yaw)*length, point_.y + cos(self.yaw)*cos(self.pitch)*length)

    def getDepthPoint(self, point_, length):
        return point(point_.x + cos(yaw)*length, point_.y + sin(self.yaw)*cos(self.pitch)*length)

    def getHeightPoint(self, point_, length):
        return point(point_.x, point_.y + sin(self.pitch)*length)

    def getWidthLine(self, point_, length):
        return lineSeg([point_, self.getWidthPoint(point_, length)])

    def getDepthLine(self, point_, length):
        return lineSeg([point_, self.getDepthPoint(point_, length)])

    def getHeigthLine(self, point_, length):
        return lineSeg([point_, self.getHeigthPoint(point_, length)])

    def draw(self, canvas):
        pass

class villa(building):
    def __init__(self, pitch, yaw, width_num, depth_num, height_num):
        super().__init__(pitch, yaw, width_num, depth_num, height_num)

    def draw(self, canvas):



