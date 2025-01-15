from point import *

class line:
    def __init__(self, x1=0,y1=0,x2=1,y2=1):
        self.ends = [point(x1,y1),point(x2,y2)]
        self.a = self.ends[1].y-self.ends[0].y
        self.b = self.ends[0].x-self.ends[1].x
        self.c = self.b*self.ends[0].y+self.a*self.ends[0].x
    
    def makeperpline(self, x1=0,y1=0):
        a2 = self.b
        b2 = -self.a
        c2 = b2*y1-a2*x1
        return a2, b2, c2

    def lineintersect(self, line):
        # -a1/b1 b2/a2 = -1
        # -a1/b1 = -a2/b2
        # -a1b2 = -a2b1
        if (self.a*line.b == line.a*self.b):
            return None #parallel, never gonna meet
        coords = mmult(self.inverse2x2(line.a,line.b), [self.c, line.c])
        return coords
    
    def inverse2x2(self, a2, b2):
        det = self.a*b2-self.b*a2
        return [[b2/det, -self.b/det], [-a2/det, self.a/det]]
