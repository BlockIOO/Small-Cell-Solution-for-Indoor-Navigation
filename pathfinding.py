import math

from node import *
from line import *

from __main__ import pythagoras, mmult

#def coords2index(x,y, region, tile_size=1):
#    return int(((x)/tile_size)+int((y)/tile_size)*(math.ceil(region[0]/tile_size)))


class network:
    #nodes = []

    def __init__(self):
        self.nodes = []
        self.lines = []
        self.borderlines = []
    
    def add(self, x=0, y=0):
        self.nodes.append(node(x, y))

    def detatch(self, node):
        for i in self.nodes[node].nodes:
            node_index = self.nodes[i].nodes.index(node)
            self.nodes[i].weights.pop(node_index)
            self.nodes[i].nodes.pop(node_index)
        self.nodes[node].nodes = []
        self.nodes[node].weights = []
    
    def delete(self, node): #can delete topmost node. Can't delete prior nodes due to how indexing and referencing other nodes are done
        self.detatch(node)
        self.nodes.pop(node)
        self.IDs -= 1
    
    def linknode(self, n1=0, n2=1):
        d = ((self.nodes[n1].x-self.nodes[n2].x)**2+(self.nodes[n1].y-self.nodes[n2].y)**2)**0.5
        self.nodes[n1].add_node(n2, d)
        self.nodes[n2].add_node(n1, d)
        
    def unlinknode(self, n1=0, n2=1):
        node_index = self.nodes[n1].nodes.index(n2)
        self.nodes[n1].weights.pop(node_index)
        self.nodes[n1].nodes.pop(node_index)
        node_index = self.nodes[n2].nodes.index(n1)
        self.nodes[n2].weights.pop(node_index)
        self.nodes[n2].nodes.pop(node_index)

    #unused
    def mark(self, node, weight=0):
        self.nodes[node].mark(weight)
    
    def info(self):
        for i in self.nodes:
            i.info()

    def line_det(self, p, l1, l2):
        return ((l2[0]-l1[0])*(p[1]-l1[1])-(l2[1]-l1[1])*(p[0]-l1[0]))>0
    
    def generate_nodes(self, rawlines, size, tolerance):
        size = size/2
        padding = size+tolerance
        paddingwalls = []
        for i in rawlines:
            self.lines.append(line(i[0],i[1],i[2],i[3]))
            self.borderlines.append(line(i[0],i[1],i[2],i[3]))
        #self.borderlines = self.lines
        
        corners = []
        wallcorners = []
        for i in self.lines:
            corners, wallcorners = self.make_border(i, corners, wallcorners, padding, size)
        #print(corners)

        # remove dots in walls
        i = 0
        while i < len(corners):
            #for j in range(len(wallcorners)-4):
            for j in range(0, len(wallcorners), 4):
                inside = self.line_det(corners[i], wallcorners[j], wallcorners[j+1])*self.line_det(corners[i], wallcorners[j+1], wallcorners[j+2])*self.line_det(corners[i], wallcorners[j+2], wallcorners[j+3])*self.line_det(corners[i], wallcorners[j+3], wallcorners[j])
                if inside == 1:
                    print('node:', i)
                    print(i, j)
                    #print(self.line_det(corners[i], wallcorners[j], wallcorners[j+1]))
                    #print(self.line_det(corners[i], wallcorners[j+1], wallcorners[j+2]))
                    #print(self.line_det(corners[i], wallcorners[j+2], wallcorners[j+3]))
                    #print(self.line_det(corners[i], wallcorners[j+3], wallcorners[j]))
                    #print(inside)
                    corners.pop(i)
                    i -= 1
                    break
            i += 1
        
        for i in corners:
            self.add(i[0], i[1])
        self.add(0, 0)
        self.add(0, 0)
        self.connectlines()

    def make_border(self, mainline, corners=[], wallcorners=[], border=1, size=0):
        q = pythagoras(mainline.ends[0].x,mainline.ends[0].y,mainline.ends[1].x,mainline.ends[1].y)
        midpoint = [(mainline.ends[0].x+mainline.ends[1].x)/2, (mainline.ends[0].y+mainline.ends[1].y)/2]
        va = [(mainline.ends[1].x-mainline.ends[0].x)/q, (mainline.ends[1].y-mainline.ends[0].y)/q]
        vb = [(mainline.ends[1].y-mainline.ends[0].y)/q, -(mainline.ends[1].x-mainline.ends[0].x)/q]
        
        temp = mmult([[va[0], va[1]],[vb[0], vb[1]]], [-(q/2+border),-border])
        temp[0] += midpoint[0]
        temp[1] += midpoint[1]
        if temp not in corners:
            corners.append(temp)
            
        temp = mmult([[va[0], va[1]],[vb[0], vb[1]]], [-(q/2+border),border])
        temp[0] += midpoint[0]
        temp[1] += midpoint[1]
        if temp not in corners:
            corners.append(temp)
            
        temp = mmult([[va[0], va[1]],[vb[0], vb[1]]], [(q/2+border),border])
        temp[0] += midpoint[0]
        temp[1] += midpoint[1]
        if temp not in corners:
            corners.append(temp)
            
        temp = mmult([[va[0], va[1]],[vb[0], vb[1]]], [(q/2+border),-border])
        temp[0] += midpoint[0]
        temp[1] += midpoint[1]
        if temp not in corners:
            corners.append(temp)
        
        #wallcorners = []
        wallcorners.append(mmult([[va[0], va[1]],[vb[0], vb[1]]], [-(q/2+size),-size]))
        wallcorners[-1][0] += midpoint[0]
        wallcorners[-1][1] += midpoint[1]
        wallcorners.append(mmult([[va[0], va[1]],[vb[0], vb[1]]], [-(q/2+size),size]))
        wallcorners[-1][0] += midpoint[0]
        wallcorners[-1][1] += midpoint[1]
        wallcorners.append(mmult([[va[0], va[1]],[vb[0], vb[1]]], [(q/2+size),size]))
        wallcorners[-1][0] += midpoint[0]
        wallcorners[-1][1] += midpoint[1]
        wallcorners.append(mmult([[va[0], va[1]],[vb[0], vb[1]]], [(q/2+size),-size]))
        wallcorners[-1][0] += midpoint[0]
        wallcorners[-1][1] += midpoint[1]
        
        for i in range(4):
            size = len(wallcorners)-4
            self.borderlines.append(line(wallcorners[size+i][0],wallcorners[size+i][1],wallcorners[size+(i+1)%4][0],wallcorners[size+(i+1)%4][1]))
            #plotline(borderlines[i])
        return corners, wallcorners

    def has_los(self, obstacle, x1=0,y1=0,x2=0,y2=0):
        s10_x = x2 - x1
        s10_y = y2 - y1
        s32_x = obstacle.ends[1].x - obstacle.ends[0].x
        s32_y = obstacle.ends[1].y - obstacle.ends[0].y

        denom = s10_x * s32_y - s32_x * s10_y

        if denom == 0 : #parallel
            return True

        denom_is_positive = denom > 0

        s02_x = x1 - obstacle.ends[0].x
        s02_y = y1 - obstacle.ends[0].y

        s_numer = s10_x * s02_y - s10_y * s02_x

        if (s_numer < 0) == denom_is_positive: #same side clockwise
            return True

        t_numer = s32_x * s02_y - s32_y * s02_x

        if (t_numer < 0) == denom_is_positive: #same side clockwise
            return True

        if ((s_numer > denom) == denom_is_positive) or ((t_numer > denom) == denom_is_positive) : # crosses
            return True
        return False

    def makelosline(self, p1,p2):
        los = True
        for k in range(len(self.borderlines)):
            los = self.has_los(self.borderlines[k], self.nodes[p1].x, self.nodes[p1].y, self.nodes[p2].x, self.nodes[p2].y)
            #print(i,j,k, los)
            if los == False:
                break
        if (los==True):
            #print(i, j)
            #borderlines.append(line(x1, y1, x2, y2))
            self.linknode(p1,p2)
            #turtle.goto(x1, y1)
            #turtle.pd()
            #turtle.goto(x2, y2)
            #turtle.pu()
        #return borderlines

    #def connectlines(dots, lines, borderlines=[]):
    def connectlines(self):
        for i in range(len(self.nodes)-2):
            #turtle.goto(dots[i][0], dots[i][1])
            #turtle.dot()
            for j in range(i+1, len(self.nodes)-2):
                self.makelosline(i, j)
                #makelosline(dots[i][0], dots[i][1], dots[j][0], dots[j][1], lines,borderlines)
        #return borderlines
            
    def trace(self, end=0):
        path = [end]
        xs = [self.nodes[end].x]
        ys = [self.nodes[end].y]
        while self.nodes[path[len(path)-1]].origin > -1:
            #print(path)
            path.append(self.nodes[path[len(path)-1]].origin)
            xs.append(self.nodes[path[len(path)-1]].x)
            ys.append(self.nodes[path[len(path)-1]].y)
        print(path)
        return path, xs, ys
    
    def bfs(self, start=0, end=1):
        for i in self.nodes:
            i.reset()
        
        queue = [start]
        tweight = [0]
        
        #print(queue)
        while ((len(queue) > 0) & (queue[0] != end)):
        #while (len(queue) > 0): # Sometimes you want to do the full map. Eg. A to C via B can be done by searching at B and then joining paths A B and B to C

            self.nodes[queue[0]].mark()
            #print(self.nodes[queue[0]].nodes)
            
            #BFS
            for i in self.nodes[queue[0]].nodes:
                if ((self.nodes[i].marked == 0) & (i not in queue)):
                    self.nodes[i].setog(queue[0])
                    queue.append(i)
            #print(queue)
            queue.pop(0)
        return self.trace(end)
    
    def djikstra(self, start=0, end=1):
        for i in self.nodes:
            i.reset()
        
        queue = [start]
        tweight = [0]
        
        #print(queue)
        #while ((len(queue) > 0) & (queue[0] != end)):
        while (len(queue) > 0): # Sometimes you want to do the full map. Eg. A to C via B can be done by searching at B and then joining paths A B and B to C

            self.nodes[queue[0]].mark(tweight[0])
            #print(self.nodes[queue[0]].nodes)

            #allnodes[queue[0]] = details of first node
            #allnodes[queue[0]].nodes[i] = node for ith neighbouring node
            #allnodes[allnodes[queue[0]].nodes[i]] = node details for ith neighbouring node
            #allnodes[queue[0]].weights[i] = ith weight for neighbouring node
            #DJIKSTRA
            for i in range(len(self.nodes[queue[0]].nodes)): #go through all neighbouring node
                if (self.nodes[self.nodes[queue[0]].nodes[i]].marked == 0): #if neighbouring node is not marked
                    tempw = tweight[0] + self.nodes[queue[0]].weights[i] #get distance for node from origin
                    search = 1
                    j = 0
                    if (self.nodes[queue[0]].nodes[i]) in queue: #if neighbouring node exists in queue
                        if (tempw < tweight[queue.index(self.nodes[queue[0]].nodes[i])]): #neighbouring node index for tweight value
                            tweight.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                            queue.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                        else:
                            search = 0
                            j = len(queue) + 2
                    while search == 1:
                        search = 0
                        if (j < len(queue)):
                            if(tweight[len(tweight)-1-j] > tempw):
                                j += 1
                                search = 1
                    if (j <= len(queue) + 1):
                        queue.insert(len(tweight)-j, self.nodes[queue[0]].nodes[i])
                        tweight.insert(len(tweight)-j, tempw)
                        self.nodes[self.nodes[queue[0]].nodes[i]].origin = queue[0]
                #print("queue")
                #print(queue)
                #print(tweight)
            tweight.pop(0)
            queue.pop(0)
        return self.trace(end)

    # Used to change heurestic to measure estimated distance remaining. abs(x2-x1)+abs(y2-y1) is another option eg. for cartesian movement
    def get_eweight(self, x=0, y=0, n1=0):
        #return abs(self.nodes[n1].x-x)+abs(self.nodes[n1].y-y)) # Taxicab distance
        return ((self.nodes[n1].x-x)**2+(self.nodes[n1].y-y)**2)**0.5 # Straight line distance

    def astar(self, start=0, end=1):
        for i in self.nodes:
            i.reset()

        endx = self.nodes[end].x
        endy = self.nodes[end].y
        
        queue = [start]
        tweight = [0]
        eweight = [self.get_eweight(endx, endy, start)]
        
        #print(queue)
        run = True
        #while ((len(queue) > 0) & (queue[0] != end)):
        while run:
            self.nodes[queue[0]].mark(tweight[0])
            #print(self.nodes[queue[0]].nodes)

            #allnodes[queue[0]] = details of first node
            #allnodes[queue[0]].nodes[i] = node for ith neighbouring node
            #allnodes[allnodes[queue[0]].nodes[i]] = node details for ith neighbouring node
            #allnodes[queue[0]].weights[i] = ith weight for neighbouring node
            #DJIKSTRA
            for i in range(len(self.nodes[queue[0]].nodes)): #go through all neighbouring node
                if (self.nodes[self.nodes[queue[0]].nodes[i]].marked == 0): #if neighbouring node is not marked
                    tempw = tweight[0] + self.nodes[queue[0]].weights[i] #get distance for node from origin 
                    tempe = tempw + self.get_eweight(endx, endy, self.nodes[queue[0]].nodes[i]) #get estimated distance of route
                    search = 1
                    j = 0
                    if (self.nodes[queue[0]].nodes[i]) in queue: #if neighbouring node exists in queue
                        if (tempw < tweight[queue.index(self.nodes[queue[0]].nodes[i])]): #neighbouring node index for tweight value
                            tweight.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                            eweight.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                            queue.pop(queue.index(self.nodes[queue[0]].nodes[i]))
                        else:
                            search = 0
                            j = len(queue) + 2
                    #Astar
                    while search == 1:
                        search = 0
                        if (j < len(queue)):
                            if(eweight[len(eweight)-1-j] > tempe):
                            #if(tweight[len(tweight)-1-j] > tempw):
                                j += 1
                                search = 1
                    if (j <= len(queue) + 1):
                        #queue.insert(len(tweight)-j, self.nodes[queue[0]].nodes[i])
                        queue.insert(len(eweight)-j, self.nodes[queue[0]].nodes[i])
                        tweight.insert(len(tweight)-j, tempw)
                        eweight.insert(len(eweight)-j, tempe)
                        self.nodes[self.nodes[queue[0]].nodes[i]].origin = queue[0]
                #print("queue")
                #print(queue)
                #print(tweight)
                #print(eweight)
            tweight.pop(0)
            eweight.pop(0)
            queue.pop(0)
            if len(queue)>0:
                if queue[0] == end:
                    self.nodes[queue[0]].mark(tweight[0])
                    run = False
            else:
                run = False
        return self.trace(end)
