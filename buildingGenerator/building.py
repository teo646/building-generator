from maskCanvas import line_seg, canvas, point
from math import tan, cos, sin, acos, atan, pi
import copy

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

    def getPoint(self, point_, pitch, yaw, length, roll = 0):
        return point(point_.x + cos(roll)*cos(yaw)*length, point_.y - (sin(yaw)*cos(roll)+sin(roll)/tan(pitch))*sin(pitch)*length)

    def getWidthPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw + pi/2, length)

    def getDepthPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw, length)

    def getHeightPoint(self, point_, length):
        return self.getPoint(point_, self.pitch+pi/2, pi/2, length)

    def draw(self, canvas):
        return canvas

class villa(building):
    roof_angle = 0.17
    width = 9
    floor_heigth = 12
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)

    def getRoofPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw, length, roll = self.roof_angle)

    def drawRoof(self, canvas):
        lines = []
        top_point = self.getHeightPoint(self.build_point, self.scale*self.floor_heigth*self.floor_num)
        top_point = self.getRoofPoint(top_point, self.scale*self.width*self.depth_num/cos(self.roof_angle))

        down_point = self.getRoofPoint(top_point, -self.scale*(self.width*self.depth_num/cos(self.roof_angle)+5))
        mask_path = [top_point,
                    down_point,
                    self.getWidthPoint(down_point, self.scale*self.width*self.width_num),
                    self.getWidthPoint(top_point, self.scale*self.width*self.width_num)]
        lines.append([top_point, down_point])
        for i in range(self.width*self.width_num):
            top_point = self.getWidthPoint(top_point, self.scale)
            down_point = self.getWidthPoint(down_point, self.scale)
            lines.append([top_point, down_point])
        canvas.registerLineSegs(lines)
        canvas.registerMask(mask_path)

        return canvas
    
    def drawWindow(self, canvas, point):
        window_heigth = 8
        window_width = 4
        lines = []
        point1 = self.getHeightPoint(point, self.scale*window_heigth)
        point2 = self.getWidthPoint(point, self.scale*window_width)
        point3 = self.getWidthPoint(point1, self.scale*window_width)
        lines.append([point, point1])
        lines.append([point2, point3])
        lines.append([point1, point3])
        canvas.registerLineSegs(lines)
        return canvas

    def drawWindows(self, canvas, build_point):
        for index in range(self.width_num):
            canvas = self.drawWindow(canvas, self.getWidthPoint(build_point, self.scale*self.width*index+2))

        return canvas

    def draw(self, canvas):
        canvas = self.drawRoof(canvas)

        lines = []
        point1 = self.build_point
        lines.append([point1, self.getHeightPoint(point1, self.scale*self.floor_heigth*self.floor_num)])
        point1 = self.getWidthPoint(self.build_point, self.scale*self.width*self.width_num)
        lines.append([point1, self.getHeightPoint(point1, self.scale*self.floor_heigth*self.floor_num)])
        point1 = self.getDepthPoint(self.build_point, self.scale*self.width*self.depth_num)
        lines.append([point1, self.getHeightPoint(point1, self.scale*(self.floor_heigth*self.floor_num+tan(self.roof_angle)*self.width*self.depth_num))])
        lines.append([self.build_point, point1])

        for floor in range(self.floor_num):
            point1 = self.getHeightPoint(self.build_point, self.scale*self.floor_heigth*floor)
            lines.append([point1, self.getWidthPoint(point1, self.scale*self.width*self.width_num)])
            canvas = self.drawWindows(canvas, point1)

        canvas.registerLineSegs(lines)
        return canvas





