from maskCanvas import line_seg, canvas, point, arc
import numpy as np
from math import tan, cos, sin, acos, atan, pi
from maskCanvas import canvas
from .straightRoof import straight_roof_left

class angled_roof_left(straight_roof_left):

    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)
        self.roof_angle = 0.2


    def drawRoof(self, canvas, build_point):
        canvas.changePen((11, 44, 154), 0.5)
        lines = []
        middle_point = self.getRoofPoint(self.getHeightPoint(self.getWidthPoint(self.build_point, -self.side_eavs_len), self.floor_height*(self.floor_num+0.5)), self.width_unit*self.depth_num/2/cos(self.roof_angle))
        back_point = self.getHeightPoint(self.getDepthPoint(self.getWidthPoint(self.build_point, -self.side_eavs_len), self.width_unit*self.depth_num), self.floor_height*(self.floor_num+0.5))
        front_point = self.getRoofPoint(middle_point, -(self.width_unit*self.depth_num/2/cos(self.roof_angle)+self.front_eavs_len))
        front_mask_path = [front_point,
                     middle_point,
                     self.getWidthPoint(middle_point, self.width_unit*self.width_num+self.side_eavs_len),
                     self.getWidthPoint(front_point, self.width_unit*self.width_num+self.side_eavs_len)]
        rear_mask_path = [middle_point,
                     back_point,
                     self.getWidthPoint(back_point, self.width_unit*self.width_num+self.side_eavs_len),
                     self.getWidthPoint(middle_point, self.width_unit*self.width_num+self.side_eavs_len)]
        lines.append([front_mask_path[0], front_mask_path[3]])
        lines.append([front_mask_path[1], front_mask_path[2]])

        for i in range(self.width_unit*self.width_num+self.side_eavs_len+1):
            f_point = self.getWidthPoint(front_point, i)
            m_point = self.getWidthPoint(middle_point, i)
            lines.append([f_point, m_point])
        canvas.registerLineSegs(lines)
        canvas.registerMask(front_mask_path)
        lines = []

        lines.append([rear_mask_path[1], rear_mask_path[2]])
        for i in range(self.width_unit*self.width_num+self.side_eavs_len+1):
            m_point = self.getWidthPoint(middle_point, i)
            b_point = self.getWidthPoint(back_point, i)
            lines.append([m_point, b_point])
        canvas.registerLineSegs(lines)
        canvas.registerMask(rear_mask_path)
        canvas.changePen((80, 80, 80), 0.3)

        return canvas

    def drawStructure(self, canvas, build_point):
        lines = []
        point1 = build_point
        point2 = self.getWidthPoint(build_point, self.width_unit*self.width_num)
        point3 = self.getDepthPoint(build_point, self.width_unit*self.depth_num)
        lines.append([point1, self.getHeightPoint(point1, self.floor_height*(self.floor_num+0.5))])
        point4 = self.getHeightPoint(point2, self.floor_height*(self.floor_num+0.5))
        lines.append([point2, point4])
        point5 = self.getHeightPoint(point3, self.floor_height*(self.floor_num+0.5))
        lines.append([point3, point5])
        lines.append([point1, point3])
        lines.append([point1, point2])

        canvas.registerLineSegs(lines)
        canvas.registerMask([point1, point2, point4, point5, point3])
        return canvas

class angled_roof_right(angled_roof_left):
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

class angled_roof_integrated(angled_roof_left):
    building_thickness_num = 3
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)

    def getMask(self, isLeft):
        point1 = self.build_point
        point2 = self.getHeightPoint(self.build_point, (self.floor_num+0.5)*self.floor_height-self.front_eavs_len*tan(self.roof_angle))
        point3 = self.getDepthPoint(self.getWidthPoint(point2, -self.front_eavs_len*cos(self.roof_angle)), -self.front_eavs_len*cos(self.roof_angle))
        point4 = self.getHeightPoint(self.getDepthPoint(self.getWidthPoint(point2,self.building_thickness_num*self.width_unit/2),self.building_thickness_num*self.width_unit/2), tan(self.roof_angle)*(self.width_unit*self.building_thickness_num/2 + self.front_eavs_len))
        point5 = self.getHeightPoint(self.getDepthPoint(self.getWidthPoint(self.build_point,self.building_thickness_num*self.width_unit),self.building_thickness_num*self.width_unit), (self.floor_num+0.5)*self.floor_height)
        offset = (isLeft - 0.5)*200*self.scale
        point6 = point(point4.x+offset, point5.y-1)
        point7 = point(point1.x+offset, point1.y)
        point2 = point(point1.x, point3.y)
        if(self.roof_angle < self.pitch):
            mask = [point1, point2, point3, point4, point5, point6, point7]
        else:
            mask = [point1, point2, point3, point4, point6, point7]

        return mask 

    def draw(self, canvas_):
        tmp_canvas = canvas()
        left_building = angled_roof_left(self.build_point, self.pitch, self.yaw, self.width_num, self.building_thickness_num, self.floor_num, self.scale)
        left_building.side_eavs_len = left_building.front_eavs_len
        #mask = self.getMask(True)
        #for i in range(len(mask)):
        #    canvas_.registerLineSeg(line_seg([mask[i-1], mask[i]], (0,0,255), 5))
        tmp_canvas.registerMask(self.getMask(True))
        tmp_canvas = left_building.draw(tmp_canvas)
        canvas_.registerLineSegs(tmp_canvas.getLines())

        tmp_canvas = canvas()
        right_building = angled_roof_right(self.build_point, self.pitch, self.yaw, self.width_num, self.building_thickness_num, self.floor_num, self.scale)
        right_building.side_eavs_len = right_building.front_eavs_len
        tmp_canvas.registerMask(self.getMask(False))
        tmp_canvas = right_building.draw(tmp_canvas)
        canvas_.registerLineSegs(tmp_canvas.getLines())
        

        return canvas_

