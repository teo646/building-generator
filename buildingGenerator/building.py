from maskCanvas import line_seg, canvas, point, arc
import numpy as np
from math import tan, cos, sin, acos, atan, pi
import copy
from maskCanvas import canvas

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
        return point(point_.x + cos(roll)*cos(yaw)*length*self.scale, point_.y - (sin(yaw)*cos(roll)*sin(pitch)+sin(roll)*cos(pitch))*length*self.scale)

    def getWidthPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw + pi/2, length)

    def getDepthPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw, length)

    def getHeightPoint(self, point_, length):
        return self.getPoint(point_, self.pitch+pi/2, pi/2, length)

    def draw(self, canvas):
        return canvas

class standard(building):
    roof_angle = 0.17
    width_unit = 9
    floor_height = 12
    window_height = 7
    window_width = 2
    side_eavs_len = 0
    front_eavs_len = 5
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)

    def getRoofPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw, length, roll = self.roof_angle)

    def drawCircle(self, canvas, center, radius, start = 0, end = 2*pi):
        canvas.registerArc(arc(center, radius*self.scale, self.pitch, self.yaw+pi/2, start, end))
        return canvas

    def drawRect(self, canvas, build_point, width, height):
        lines = []
        point0 = build_point
        point1 = self.getHeightPoint(point0, height)
        point2 = self.getWidthPoint(point0, width)
        point3 = self.getHeightPoint(point2, height)
        canvas.registerLineSeg([point0, point1])
        canvas.registerLineSeg([point0, point2])
        canvas.registerLineSeg([point1, point3])
        canvas.registerLineSeg([point2, point3])
        return canvas

    def getRotatePoint(self, canvas, point_, length, roll):
        return self.getPoint(point_, self.pitch, self.yaw + pi/2, length, roll)

    def drawRoof(self, canvas, build_point):
        canvas.changePen((11, 44, 154), 0.5)
        lines = []
        self.getHeightPoint(self.build_point, self.floor_height*(self.floor_num+0.5))
        top_point = self.getRoofPoint(self.getHeightPoint(self.getWidthPoint(self.build_point, -self.side_eavs_len), self.floor_height*(self.floor_num+0.5)), self.width_unit*self.depth_num/cos(self.roof_angle))
        down_point = self.getRoofPoint(top_point, -(self.width_unit*self.depth_num/cos(self.roof_angle)+self.front_eavs_len))
        mask_path = [top_point,
                    down_point,
                    self.getWidthPoint(down_point, self.width_unit*self.width_num+self.side_eavs_len),
                    self.getWidthPoint(top_point, self.width_unit*self.width_num+self.side_eavs_len)]
        lines.append([top_point, down_point])
        lines.append([top_point, mask_path[3]])
        lines.append([down_point, mask_path[2]])

        for i in range(self.width_unit*self.width_num+self.side_eavs_len):
            top_point = self.getWidthPoint(top_point, 1)
            down_point = self.getWidthPoint(down_point, 1)
            lines.append([top_point, down_point])
        canvas.registerLineSegs(lines)
        canvas.registerMask(mask_path)
        canvas.changePen((80,80,80), 0.3)

        return canvas
    
    def drawSimpleDeco(self, canvas, build_point):
        top_point = self.getWidthPoint(self.getHeightPoint(build_point, self.window_height+1), -0.5)
        #drawing top decoration
        canvas = self.drawRect(canvas, top_point, self.window_width+2, 0.5)
        return canvas

    def drawFancyDeco(self, canvas, build_point):
        center = self.getWidthPoint(self.getHeightPoint(build_point, self.window_height+0.5), self.window_width/2 + 0.5)

        small_angle = atan(0.5/(self.window_width/2 +0.5))
        small_radius = np.sqrt(0.5**2 + (self.window_width/2+0.5)**2)
        canvas = self.drawCircle(canvas, center, small_radius, small_angle, pi-small_angle)

        big_radius = np.sqrt(0.5**2 + (self.window_width/2+1)**2)
        canvas = self.drawCircle(canvas, center, big_radius, small_angle, pi-small_angle)

        deco_unit = (pi-2*small_angle)/8
        for roll in np.arange(small_angle, pi-small_angle+deco_unit, deco_unit):
            canvas.registerLineSeg([self.getRotatePoint(canvas, center, small_radius, roll), self.getRotatePoint(canvas, center, big_radius, roll)])

        center = self.getHeightPoint(center, 0.5+(small_radius-0.5)/2)
        canvas = self.drawCircle(canvas, center, (small_radius-0.5)/2)
        return canvas



    def drawWindow(self, canvas, build_point):
        #drawing frame
        canvas = self.drawRect(canvas, build_point, self.window_width+1, self.window_height+1)
        window_point = self.getWidthPoint(self.getHeightPoint(build_point, 0.5), 0.5)
        #drawing window
        canvas = self.drawRect(canvas, window_point, self.window_width, self.window_height)
        return canvas


    def drawFloor(self, canvas, build_point):
        for index in range(self.width_num):
            point1 = self.getWidthPoint(build_point, (self.width_unit*index+3))
            canvas = self.drawWindow(canvas, point1)
            canvas = self.drawSimpleDeco(canvas, point1)
        return canvas

    def drawSecondFloor(self, canvas, build_point):
        for index in range(self.width_num):
            point1 = self.getWidthPoint(build_point, (self.width_unit*index+3))
            canvas = self.drawWindow(canvas, point1)
            canvas = self.drawFancyDeco(canvas, point1)
        return canvas

    def drawStructure(self, canvas, build_point):
        lines = []
        point1 = build_point
        point2 = self.getWidthPoint(build_point, self.width_unit*self.width_num)
        point3 = self.getDepthPoint(build_point, self.width_unit*self.depth_num)
        lines.append([point1, self.getHeightPoint(point1, self.floor_height*(self.floor_num+0.5))])
        point4 = self.getHeightPoint(point2, self.floor_height*(self.floor_num+0.5))
        lines.append([point2, point4])
        point5 = self.getHeightPoint(point3, self.floor_height*(self.floor_num+0.5)+tan(self.roof_angle)*self.width_unit*self.depth_num)
        lines.append([point3, point5])
        lines.append([point1, point3])
        lines.append([point1, point2])

        canvas.registerLineSegs(lines)
        canvas.registerMask([point1, point2, point4, point5, point3])
        return canvas

    def drawDoor(self, canvas, build_point):
        lines = []
        point1 =build_point
        lines.append([point1, self.getHeightPoint(point1, self.floor_height/2+8-2)])
        point2 = self.getWidthPoint(point1, 1)
        lines.append([point2, self.getHeightPoint(point2, self.floor_height/2+8-2)])
        point3 = self.getWidthPoint(point2, 5)
        lines.append([point3, self.getHeightPoint(point3, self.floor_height/2+8-2)])
        point4 = self.getWidthPoint(point3, 1)
        lines.append([point4, self.getHeightPoint(point4, self.floor_height/2+8-2)])


        point5 = self.getWidthPoint(self.getHeightPoint(point2, self.floor_height/2+8-2), 2.5)
        canvas = self.drawCircle(canvas, point5, 2.5, 0, pi)
        canvas = self.drawCircle(canvas, point5, 3.5, 0, pi)
        for roll in np.arange(0, pi+0.1, pi/5):
            lines.append([point5, self.getRotatePoint(canvas, point5, 2.5, roll)])


        canvas.registerLineSegs(lines)

        decoration_point = self.getWidthPoint(self.getHeightPoint(build_point, 0.5), 1.5)
        canvas = self.drawRect(canvas, decoration_point, 1.5, 4.5)
        decoration_point = self.getWidthPoint(decoration_point, 2.5)
        canvas = self.drawRect(canvas, decoration_point, 1.5, 4.5)
        decoration_point = self.getHeightPoint(decoration_point, 6.5)
        canvas = self.drawRect(canvas, decoration_point, 1.5, 4.5)
        decoration_point = self.getWidthPoint(decoration_point, -2.5)
        canvas = self.drawRect(canvas, decoration_point, 1.5, 4.5)
        decoration_point = self.getWidthPoint(self.getHeightPoint(decoration_point, -1), 0.5)
        canvas = self.drawCircle(canvas, decoration_point, 0.3)
        canvas = self.drawCircle(canvas, decoration_point, 0.15)

        return canvas

    def drawFirstFloor(self, canvas, build_point):
        for index in range(self.width_num):
            if( index == 3):
                canvas = self.drawDoor(canvas, self.getWidthPoint(build_point, self.width_unit*index + 1))
            else:
                canvas = self.drawWindow(canvas, self.getHeightPoint(self.getWidthPoint(build_point, (self.width_unit*index+3)), self.floor_height/2))
        return canvas


    def drawWall(self, canvas, build_point):
        canvas = self.drawFirstFloor(canvas, build_point)
        for floor in range(1, self.floor_num):
            point1 = self.getHeightPoint(build_point, self.floor_height*floor + self.floor_height/2)
            canvas.registerLineSeg([point1, self.getWidthPoint(point1, self.width_unit*self.width_num)])
            if(floor == 1):
                canvas = self.drawSecondFloor(canvas, point1)
            else:
                canvas = self.drawFloor(canvas, point1)


        return canvas


    def draw(self, canvas):
        canvas.changePen((80,80,80), 0.3)
        canvas = self.drawRoof(canvas, self.build_point)
        canvas = self.drawWall(canvas, self.build_point)
        canvas = self.drawStructure(canvas, self.build_point)

        return canvas


class opposite_dir(standard):
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

class integrated(standard):
    building_thickness_num = 3
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)

    def getMask(self, isRight):
        point1 = self.build_point
        point2 = self.getHeightPoint(self.build_point, (self.floor_num+0.5)*self.floor_height-self.front_eavs_len*tan(self.roof_angle))
        point3 = self.getDepthPoint(self.getWidthPoint(point2, -self.front_eavs_len*cos(self.roof_angle)), -self.front_eavs_len*cos(self.roof_angle))
        point4 = self.getHeightPoint(self.getDepthPoint(self.getWidthPoint(point2,self.building_thickness_num*self.width_unit),self.building_thickness_num*self.width_unit), tan(self.roof_angle)*(self.width_unit*self.building_thickness_num + self.front_eavs_len))
        offset = (isRight - 0.5)*200*self.scale
        point5 = point(point4.x+offset, point4.y)
        point6 = point(point1.x+offset, point1.y)
        point2 = point(point1.x, point3.y)
        mask = [point1, point2, point3, point4, point5, point6]
        return mask 

    def draw(self, canvas_):
        tmp_canvas = canvas()
        standard_side = standard(self.build_point, self.pitch, self.yaw, self.width_num, self.building_thickness_num, self.floor_num, self.scale)
        standard_side.side_eavs_len = standard_side.front_eavs_len
        #mask_p0 = self.build_point
        #mask_p1 = self.getHeightPoint(mask_p0, self.floor_height*(self.floor_num+0.5))
        #mask_p2 = self.getHeightPoint(self.getDepthPoint(self.getWidthPoint(mask_p1,self.building_thickness_num*self.width_unit),self.building_thickness_num*self.width_unit), tan(self.roof_angle)*self.width_unit*self.building_thickness_num)
        #mask_p3 = self.getHeightPoint(self.getWidthPoint(mask_p2, -self.building_thickness_num*self.width_unit-1), 1)
        #mask_p4 = self.getHeightPoint(mask_p3, -self.floor_height*(self.floor_num+0.5)-tan(self.roof_angle)*self.width_unit*self.depth_num)
        tmp_canvas.registerMask(self.getMask(True))
        tmp_canvas = standard_side.draw(tmp_canvas)
        canvas_.registerLineSegs(tmp_canvas.getLines())

        tmp_canvas = canvas()
        opposite_side = opposite_dir(self.build_point, self.pitch, self.yaw, self.width_num, self.building_thickness_num, self.floor_num, self.scale)
        opposite_side.side_eavs_len = opposite_side.front_eavs_len
        #mask_p3 = self.getHeightPoint(self.getDepthPoint(mask_p2, -self.building_thickness_num*self.width_unit-1), 1)
        #mask_p4 = self.getHeightPoint(mask_p3, -self.floor_height*(self.floor_num+0.5)-tan(self.roof_angle)*self.width_unit*self.depth_num)
        tmp_canvas.registerMask(self.getMask(False))
        tmp_canvas = opposite_side.draw(tmp_canvas)
        canvas_.registerLineSegs(tmp_canvas.getLines())
        

        return canvas_

