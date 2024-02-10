from maskCanvas import line_seg, canvas, point, arc
import numpy as np
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
        return point(point_.x + cos(roll)*cos(yaw)*length*self.scale, point_.y - (sin(yaw)*cos(roll)*sin(pitch)+sin(roll)*cos(pitch))*length*self.scale)

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
    floor_height = 12
    window_height = 7
    window_width = 2
    def __init__(self, build_point, pitch, yaw, width_num, depth_num, floor_num, scale=1):
        super().__init__(build_point, pitch, yaw, width_num, depth_num, floor_num, scale)

    def getRoofPoint(self, point_, length):
        return self.getPoint(point_, self.pitch, self.yaw, length, roll = self.roof_angle)

    def drawRectOnFront(self, canvas, build_point, width, height):
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


    def drawRoof(self, canvas, build_point):
        lines = []
        top_point = self.getRoofPoint(build_point, self.width*self.depth_num/cos(self.roof_angle))
        down_point = self.getRoofPoint(top_point, -(self.width*self.depth_num/cos(self.roof_angle)+5))
        mask_path = [top_point,
                    down_point,
                    self.getWidthPoint(down_point, self.width*self.width_num),
                    self.getWidthPoint(top_point, self.width*self.width_num)]
        lines.append([top_point, down_point])
        lines.append([top_point, mask_path[3]])
        lines.append([down_point, mask_path[2]])

        for i in range(self.width*self.width_num):
            top_point = self.getWidthPoint(top_point, 1)
            down_point = self.getWidthPoint(down_point, 1)
            lines.append([top_point, down_point])
        canvas.registerLineSegs(lines)
        canvas.registerMask(mask_path)

        return canvas
    
    def drawSimpleDeco(self, canvas, build_point):
        top_point = self.getWidthPoint(self.getHeightPoint(build_point, self.window_height+1), -0.5)
        #drawing top decoration
        canvas = self.drawRectOnFront(canvas, top_point, self.window_width+2, 0.5)
        return canvas

    def drawFancyDeco(self, canvas, build_point):
        center = self.getWidthPoint(self.getHeightPoint(build_point, self.window_height+0.5), self.window_width/2 + 0.5)

        small_angle = atan(0.5/(self.window_width/2 +0.5))
        small_radius = np.sqrt(0.5**2 + (self.window_width/2+0.5)**2)
        canvas.registerArc(arc(center, small_radius*self.scale, self.pitch, self.yaw+pi/2, small_angle, pi-small_angle))

        big_radius = np.sqrt(0.5**2 + (self.window_width/2+1)**2)
        canvas.registerArc(arc(center, big_radius*self.scale, self.pitch, self.yaw+pi/2, small_angle, pi-small_angle))

        deco_unit = (pi-2*small_angle)/8
        for roll in np.arange(small_angle, pi-small_angle+deco_unit, deco_unit):
            canvas.registerLineSeg([self.getPoint(center, self.pitch, self.yaw + pi/2, small_radius, roll), self.getPoint(center, self.pitch, self.yaw + pi/2, big_radius, roll)])

        center = self.getHeightPoint(center, 0.5+(small_radius-0.5)/2)
        canvas.registerArc(arc(center, (small_radius-0.5)/2*self.scale, self.pitch, self.yaw+pi/2))
        return canvas



    def drawWindow(self, canvas, build_point):
        #drawing frame
        canvas = self.drawRectOnFront(canvas, build_point, self.window_width+1, self.window_height+1)
        window_point = self.getWidthPoint(self.getHeightPoint(build_point, 0.5), 0.5)
        #drawing window
        canvas = self.drawRectOnFront(canvas, window_point, self.window_width, self.window_height)
        return canvas


    def drawFloor(self, canvas, build_point):
        for index in range(self.width_num):
            point1 = self.getWidthPoint(build_point, (self.width*index+3.5))
            canvas = self.drawWindow(canvas, point1)
            canvas = self.drawSimpleDeco(canvas, point1)
        return canvas

    def drawSecondFloor(self, canvas, build_point):
        for index in range(self.width_num):
            point1 = self.getWidthPoint(build_point, (self.width*index+3.5))
            canvas = self.drawWindow(canvas, point1)
            canvas = self.drawFancyDeco(canvas, point1)
        return canvas

    def drawStructure(self, canvas, build_point):
        lines = []
        point1 = build_point
        point2 = self.getWidthPoint(build_point, self.width*self.width_num)
        point3 = self.getDepthPoint(build_point, self.width*self.depth_num)
        lines.append([point1, self.getHeightPoint(point1, self.floor_height*(self.floor_num+0.5))])
        lines.append([point2, self.getHeightPoint(point2, self.floor_height*(self.floor_num+0.5))])
        lines.append([point3, self.getHeightPoint(point3, self.floor_height*(self.floor_num+0.5)+tan(self.roof_angle)*self.width*self.depth_num)])
        lines.append([point1, point3])
        lines.append([point1, point2])

        canvas.registerLineSegs(lines)
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
        canvas.registerArc(arc(point5, 2.5*self.scale, self.pitch, self.yaw+pi/2, 0, pi))
        canvas.registerArc(arc(point5, 3.5*self.scale, self.pitch, self.yaw+pi/2, 0, pi))
        for roll in np.arange(0, pi+0.1, pi/5):
            lines.append([point5, self.getPoint(point5, self.pitch, self.yaw + pi/2, 2.5, roll)])


        canvas.registerLineSegs(lines)

        decoration_point = self.getWidthPoint(self.getHeightPoint(build_point, 0.5), 1.5)
        canvas = self.drawRectOnFront(canvas, decoration_point, 1.5, 4.5)
        decoration_point = self.getWidthPoint(decoration_point, 2.5)
        canvas = self.drawRectOnFront(canvas, decoration_point, 1.5, 4.5)
        decoration_point = self.getHeightPoint(decoration_point, 6.5)
        canvas = self.drawRectOnFront(canvas, decoration_point, 1.5, 4.5)
        decoration_point = self.getWidthPoint(decoration_point, -2.5)
        canvas = self.drawRectOnFront(canvas, decoration_point, 1.5, 4.5)
        decoration_point = self.getWidthPoint(self.getHeightPoint(decoration_point, -1), 0.5)
        canvas.registerArc(arc(decoration_point, 0.3*self.scale, self.pitch, self.yaw+pi/2))
        canvas.registerArc(arc(decoration_point, 0.15*self.scale, self.pitch, self.yaw+pi/2))

        return canvas

    def drawFirstFloor(self, canvas, build_point):
        for index in range(self.width_num):
            if( index == 3):
                canvas = self.drawDoor(canvas, self.getWidthPoint(build_point, self.width*index + 1))
            else:
                canvas = self.drawWindow(canvas, self.getHeightPoint(self.getWidthPoint(build_point, (self.width*index+3.5)), self.floor_height/2))
        return canvas


    def drawWall(self, canvas, build_point):
        canvas = self.drawFirstFloor(canvas, build_point)
        for floor in range(1, self.floor_num):
            point1 = self.getHeightPoint(build_point, self.floor_height*floor + self.floor_height/2)
            canvas.registerLineSeg([point1, self.getWidthPoint(point1, self.width*self.width_num)])
            if(floor == 1):
                canvas = self.drawSecondFloor(canvas, point1)
            else:
                canvas = self.drawFloor(canvas, point1)


        return canvas


    def draw(self, canvas):
        canvas = self.drawRoof(canvas, self.getHeightPoint(self.build_point, self.floor_height*(self.floor_num+0.5)))
        canvas = self.drawStructure(canvas, self.build_point)
        canvas = self.drawWall(canvas, self.build_point)

        return canvas





