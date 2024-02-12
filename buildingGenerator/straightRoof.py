from maskCanvas import line_seg, canvas, point, arc
import numpy as np
from math import tan, cos, sin, acos, atan, pi
from maskCanvas import canvas
from .standard import standard

straight_roof_left = standard

class straight_roof_right(straight_roof_left):
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)
    
    def getRoofPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw+pi/2, length, roll = self.roof_angle)

    def drawCircle(self, canvas, center, radius, start = 0, end = 2*pi):
        canvas.registerArc(arc(center, radius*self.scale, self.pitch, self.yaw, start, end))
        return canvas

    def getRotatePoint(self, canvas, point_, length, roll):
        return self.getPoint(point_, self.pitch, self.yaw, length, roll)

    def draw(self, canvas):
        tmp = self.getWidthPoint
        self.getWidthPoint = self.getDepthPoint
        self.getDepthPoint = tmp
        canvas.changePen((80,80,80), 0.3)
        canvas = self.drawRoof(canvas, self.getHeightPoint(self.build_point, self.floor_height*(self.floor_num+0.5)))
        canvas = self.drawWall(canvas, self.build_point)
        canvas = self.drawStructure(canvas, self.build_point)

        return canvas

class straight_roof_integrated(straight_roof_left):
    building_thickness_num = 3
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)

    def getMask(self, isLeft):
        point1 = self.build_point
        point2 = self.getHeightPoint(self.build_point, (self.floor_num+0.5)*self.floor_height-self.front_eavs_len*tan(self.roof_angle))
        point3 = self.getDepthPoint(self.getWidthPoint(point2, -self.front_eavs_len*cos(self.roof_angle)), -self.front_eavs_len*cos(self.roof_angle))
        point4 = self.getHeightPoint(self.getDepthPoint(self.getWidthPoint(point2,self.building_thickness_num*self.width_unit),self.building_thickness_num*self.width_unit), tan(self.roof_angle)*(self.width_unit*self.building_thickness_num + self.front_eavs_len))
        offset = (isLeft - 0.5)*200*self.scale
        point5 = point(point4.x+offset, point4.y-1)
        point6 = point(point1.x+offset, point1.y)
        point2 = point(point1.x, point3.y)
        mask = [point1, point2, point3, point4, point5, point6]
        return mask 

    def draw(self, canvas_):
        tmp_canvas = canvas()
        left_building = straight_roof_left(self.build_point, self.pitch, self.yaw, self.width_num, self.building_thickness_num, self.floor_num, self.scale)
        left_building.side_eavs_len = left_building.front_eavs_len
        tmp_canvas.registerMask(self.getMask(True))
        tmp_canvas = left_building.draw(tmp_canvas)
        canvas_.registerLineSegs(tmp_canvas.getLines())

        tmp_canvas = canvas()
        right_building = straight_roof_right(self.build_point, self.pitch, self.yaw, self.width_num, self.building_thickness_num, self.floor_num, self.scale)
        right_building.side_eavs_len = right_building.front_eavs_len
        tmp_canvas.registerMask(self.getMask(False))
        tmp_canvas = right_building.draw(tmp_canvas)
        canvas_.registerLineSegs(tmp_canvas.getLines())
        

        return canvas_

