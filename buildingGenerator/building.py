from maskCanvas import line_seg, canvas, point
from math import cos, sin, pi

#
class building:
    
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale):
        self.build_point = build_point
        self.yaw = yaw
        self.pitch = pitch
        self.width_num = width_num
        self.depth_num = depth_num
        self.floor_num = floor_num
        self.scale = scale

    def getPoint(self, point_, pitch, yaw, length):
        return point(point_.x + cos(yaw)*length, point_.y + sin(yaw)*cos(pitch)*length)

    def getWidthPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw + pi/2, length)

    def getDepthPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw, length)

    def getHeightPoint(self, point_, length):
        return self.getPoint(point_, self.pitch+pi/2, pi/2, length)

    def draw(self, canvas):
        return canvas

class villa(building):
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)

    def getRoofPoint(self, point_, length):
        return self.getPoint(point_, self.pitch - pi/6, self.yaw, length)

    def getRoof(self):
        lines = []
        top_point = self.getHeightPoint(self.build_point, self.scale*10*self.floor_num)
        top_point = self.getRoofPoint(top_point, self.scale*8*self.depth_num/cos(0.25))

        down_point = self.getRoofPoint(top_point, -self.scale*(8*self.depth_num/cos(0.25)+4))
        lines.append([top_point, down_point])
        for i in range(12*self.width_num):
            top_point = self.getWidthPoint(top_point, self.scale)
            down_point = self.getWidthPoint(down_point, self.scale)
            lines.append([top_point, down_point])
        return lines


    def getDrawing(self):
        lines = []





