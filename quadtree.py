class Quadtree():
    def __init__(self, point, x1, y1, x2, y2):

        self.point = point
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.c1, self.c2, self.c3, self.c4 = None, None, None, None

    def getPoint(self):
        return self.point


    def getChild(self, quadrant):
        if quadrant == 1: return self.c1
        if quadrant == 2: return  self.c2
        if quadrant == 3: return self.c3
        if quadrant == 4: return  self.c4
        return None

    def hasChild(self, quadrant):
        return (quadrant == 1 and self.c1 is not None) or (quadrant == 2 and self.c2 is not None) or (quadrant == 3 and self.c3 is not None) or (quadrant == 4 and self.c4 is not None)


    def insert(self, point):
        if point.x >= self.point.x and point.y <= self.point.y:
            if self.hasChild(1):
                self.getChild(1).insert(point)
            else:
                self.c1 = Quadtree(point, self.point.x, self.y1, self.x2, self.point.y)
        if point.x > self.point.x and point.y > self.point.y:
            if self.hasChild(4):
                self.getChild(4).insert(point)
            else:
                self.c4 = Quadtree(point, self.point.x, self.point.y, self.x2, self.y2)
        if point.x < self.point.x and point.y < self.point.y:
            if self.hasChild(2):
                self.getChild(2).insert(point)
            else:
                self.c2 = Quadtree(point, self.x1, self.y1, self.point.x, self.point.y)
        if point.x <= self.point.x and point.y >= self.point.y:
            if self.hasChild(3):
                self.getChild(3).insert(point)
            else:
                self.c3 = Quadtree(point, self.x1, self.point.y, self.point.x, self.y2)
