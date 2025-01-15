import turtle
import math

from __main__ import allnodes, wireless
from __main__ import calculateDistance, inverse2x2, mmult, pythagoras, time2distance

class model():
    def __init__(self, region=[10, 10], lines = [], small_cells=[[5, -5], [-5, 0], [5, 5]], c = 300000000, sample_rate = 1000000000, step = 1, tolerance = 1):
        #setup
        self.region = region #scale = 1m
        self.lines = lines
        self.small_cells = small_cells
        self.c = c #speed of signal
        self.sample_rate = sample_rate #samples per second
        #self.move_target()
        self.rx, self.ry = region[0]/2, region[1]/2
        self.tx, self.ty = region[0]/2, region[1]/2
        allnodes.nodes[len(allnodes.nodes)-2].x = self.rx
        allnodes.nodes[len(allnodes.nodes)-2].y = self.ry
        allnodes.nodes[len(allnodes.nodes)-1].x = self.tx
        allnodes.nodes[len(allnodes.nodes)-1].y = self.ty
        for i in range(len(allnodes.nodes)-1):
            allnodes.makelosline(len(allnodes.nodes)-1, i)
        self.wwidth, self.wheight = 0, 0
        self.step = step
        self.tolerance = tolerance
        self.finished = 0
        self.turtle_setup()
    
    def measure_plm(self):
        #get distances and convert to power to simulate
        self.measurements = []
        for i in range(len(self.small_cells)):
            self.measurements.append(distance2w(pythagoras(self.rx,self.ry,self.small_cells[i][0],self.small_cells[i][1])))

    def measure_tx_toa(self, animate=1):
        #transmit from robot
        #beacons = 0
        step = 1/self.sample_rate #time step size
        radius = 0 #time radius not distance radius
        cells = []
        found_cells = []
        self.measurements = []
        for i in range(len(self.small_cells)):
            cells.append(i)
            self.measurements.append(0)
        temp_dist = []
        #get distances to reference to know when the signal has passed reciever. This marks when the reciever has picked up a signal
        for i in cells:
            temp_dist.append(pythagoras(self.rx,self.ry,self.small_cells[i][0],self.small_cells[i][1]))
        #print(cells)
        #print(temp_dist)
        ct = 0
        while(len(cells) > 0):
            ct += 1            
            radius = ct*step
            for i in cells:
                if temp_dist[i] <= (self.c*radius): #distance = speed * time
                    #print(i)
                    found_cells.append(i)
                    cells.pop(cells.index(i))
                    #beacons += 1
                    self.measurements[i] = radius
                    #print(self.measurements)
                    #print(radius, self.c*radius)
                    
            if (animate == 1):
                self.workings.color('#0000FF')
                self.workings.clear()
                self.circle(self.rx, self.ry, radius*self.c, turtle=self.workings)
                self.workings.color('#FF0000')
                for j in range(len(found_cells)):
                    self.circle(self.rx, self.ry, self.measurements[found_cells[j]]*self.c, turtle=self.workings)
        if (animate == 1):
            self.workings.clear()
            
    
    def measure_rx_toa(self, animate=1):
        #transmit from RTL-SDR
        #beacons = 0
        step = 1/self.sample_rate #time step size
        radius = 0 #time radius not distance radius
        cells = []
        found_cells = []
        self.measurements = []
        for i in range(len(self.small_cells)):
            cells.append(i)
            self.measurements.append(0)
        temp_dist = []
        #get distances to reference to know when the signal has passed robot. This marks when the robot has picked up a signal
        for i in cells:
            temp_dist.append(pythagoras(self.rx,self.ry,self.small_cells[i][0],self.small_cells[i][1]))
        #print(cells)
        #print(temp_dist)
        ct = 0
        while(len(cells) > 0):
            ct += 1            
            radius = ct*step
            for i in cells:
                if temp_dist[i] <= (self.c*radius): #distance = speed * time
                    #print(i)
                    found_cells.append(i)
                    cells.pop(cells.index(i))
                    #beacons += 1
                    self.measurements[i] = radius
                    #print(self.measurements)
                    #print(radius, self.c*radius)
            
            if (animate == 1):
                self.workings.color('#0000FF')
                self.workings.clear()
                for j in cells:
                    self.circle(self.small_cells[j][0], self.small_cells[j][1], radius*self.c, turtle=self.workings)
                self.workings.color('#FF0000')
                for j in range(len(found_cells)):
                    self.circle(self.small_cells[found_cells[j]][0], self.small_cells[found_cells[j]][1], self.measurements[found_cells[j]]*self.c, turtle=self.workings)
        if (animate == 1):
            self.workings.clear()
    
    def get_plm_distances(self):
        #convert power to distance
        self.distances = []
        size = len(self.measurements)
        for i in range(size):
            self.distances.append(w2distance(self.measurements[i]))

    def get_toa_distances(self):
        #convert power to distance
        self.distances = []
        size = len(self.measurements)
        for i in range(size):
            self.distances.append(time2distance(self.measurements[i], self.c))
    
    def find_intersections(self):
        self.intersections = []
        #size = len(self.measurements)
        for i in range(3):
            self.intersections.append(self.matrix_intersections(i))
        return
        """
        for i in range(size):
            self.intersections.append(doublecircle(self.small_cells[i%size][0],self.small_cells[i%size][1],self.distances[i],self.small_cells[(i+1)%size][0],self.small_cells[(i+1)%size][1],self.distances[(i+1)%size]))
            #temp = doublecircle(self.small_cells[i%size][0],self.small_cells[i%size][1],self.distances[i],self.small_cells[(i+1)%size][0],self.small_cells[(i+1)%size][1],self.distances[(i+1)%size])
            #self.intersections.append(temp[0])
            #self.intersections.append(temp[1])
        #print(self.distances)
        """

    
    def matrix_intersections(self, n=0):
        x1 = self.small_cells[(0+n)%3][0]
        y1 = self.small_cells[(0+n)%3][1]
        x2 = self.small_cells[(1+n)%3][0]
        y2 = self.small_cells[(1+n)%3][1]
        x3 = self.small_cells[(2+n)%3][0]
        y3 = self.small_cells[(2+n)%3][1]
        #print(self.small_cells[0])
        d1 = self.distances[(0+n)%3]
        d2 = self.distances[(1+n)%3]
        d3 = self.distances[(2+n)%3]
        #print(self.small_cells[0][1])
        #print(self.distances)
        inverse = inverse2x2([[2*(x1-x2), 2*(y1-y2)],[2*(x1-x3), 2*(y1-y3)]])
        #print("Inverse:", inverse)
        constants = [x1**2-(x2**2)+y1**2-(y2**2)-(d1**2)+d2**2, x1**2-(x3**2)+y1**2-(y3**2)-(d1**2)+d3**2]
        #print("Constants:", constants)
        coords = mmult(inverse, constants)
        #print("coordinates:", coords)
        #print("error:", pythagoras(coords[0], coords[1], self.location[0], self.location[1]))
        return coords

    def mean_distance(self):
        size = len(self.intersections)
        x = 0
        y = 0
        for i in range(size):
            x += self.intersections[i][0]
            y += self.intersections[i][1]
        x = x/size
        y = y/size
        return [x, y]
        
        """
        size = len(self.intersections)
        mean_distance = []
        totalx = []
        totaly = []
        for i in range(2**size):
            totalx.append(0)
            totaly.append(0)
            for j in range(size):
                totalx[-1] += self.intersections[j][(i>>j)&1][0]
                totaly[-1] += self.intersections[j][(i>>j)&1][1]
            totalx[-1] /= size
            totaly[-1] /= size
            mean_distance.append(0)
            for j in range(size):
                mean_distance[-1] += pythagoras(totalx[-1],totaly[-1],self.intersections[j][(i>>j)&1][0],self.intersections[j][(i>>j)&1][1])
            mean_distance[-1] /= size
        #minimum = min(mean_distance)
        #min_index = mean_distance.index(minimum)
        min_index = mean_distance.index(min(mean_distance))
        self.location = [totalx[min_index], totaly[min_index]]
        """
        
    def locate(self):
        #self.get_plm_distances()
        self.get_toa_distances()
        self.find_intersections()
        try:
            coords = self.mean_distance()
            return coords
        except:
            print('error')
            print(self.rx, self.ry, self.distances, self.intersections)
    
    def wireless_locate(self):
        #convert power to distance
        self.distances = []
        strengths = []
        #for i in wireless.ue:
        for i in range(len(wireless.ue)):
            strengths.append(wireless.ue[i].calculateSINR(wireless.bs, wireless.obstacles))
            self.distances.append(calculateDistance(strengths[i]))
            #print(calculateDistance(strengths[i]))
        self.find_intersections()
        try:
            coords = self.mean_distance()
            print('actual location:', self.rx, self.ry)
            print('calculated location:', coords)
            print('error:', pythagoras(self.rx, self.ry, coords[0], coords[1]))
            return coords
        except:
            print('error')
            print(self.rx, self.ry, self.distances, self.intersections)

    def reconnect(self):
        wireless.bs[0].x = self.rx
        wireless.bs[0].y = self.ry
        wireless.connectUsersToTheBestBS(wireless.obstacles)
        self.location = self.wireless_locate()
        
    
    def move_target(self):
        self.rx, self.ry = random.randint(0, self.region[0]), random.randint(0, self.region[1])
        #self.rx, self.ry = random.randint(-self.region[0]/2, self.region[0]/2), random.randint(-self.region[1]/2, self.region[1]/2)
        #self.rx = random.randint(-self.region[0]/2, self.region[0]/2)
        #self.ry = random.randint(-self.region[1]/2, self.region[1]/2)
        
################################TURTLE FUNCTIONS############################
    
    def size_window(self):
        wwidth = turtle.window_width()
        wheight = turtle.window_height()
        return wwidth, wheight
    
    def get_scale(self):
        #scale factor so screen is a reasonable size and offset so corner is 0,0 instead of centre for math reasons
        wratio = self.wwidth/self.wheight
        rratio = self.region[0]/self.region[1]
        #smaller ratio = taller
        #larger ratio = wider
        self.scale = [0,0,0]
        self.scale[0] = self.region[0]/2
        self.scale[1] = self.region[1]/2
        if rratio > wratio:
            #print('wider')
            self.scale[2] = 0.9*self.wwidth/self.region[0]
        #print('taller')
        else:
            self.scale[2] = 0.9*self.wheight/self.region[1]

    def toscale(self, x, y):
        return (x-self.scale[0])*self.scale[2],(y-self.scale[1])*self.scale[2]
    
    def fromscale(self, x, y):
        return x/self.scale[2]+self.scale[0],y/self.scale[2]+self.scale[1]
    
    def gotoscale(self, x, y, turtle=turtle):
        x2, y2 = self.toscale(x, y)
        turtle.goto(x2, y2)

    def point(self, display, letter, x=0, y=0, color='#000000', turtle=turtle):
        location = self.fromscale(turtle.xcor(), turtle.ycor())
        #location = [(turtle.xcor()+self.scale[0])/self.scale[2], (turtle.ycor()+self.scale[1])/self.scale[2]]
        #location = [x, y]
        turtle.color(color)
        if display%2 == 1:
            turtle.write(letter)
            #print(letter, ":", location)
        if display > 1:
            turtle.dot()
        turtle.color('#000000')
        return location
    
    def make_box(self, turtle=turtle):
        turtle.pu()
        self.gotoscale(0, 0, turtle=turtle)
        turtle.pd()
        self.gotoscale(self.region[0], 0, turtle=turtle)
        self.point(3, '(%d, %d)' % (self.region[0], 0), turtle=turtle)
        self.gotoscale(self.region[0], self.region[1], turtle=turtle)
        self.point(3, '(%d, %d)' % (self.region[1], self.region[1]), turtle=turtle)
        self.gotoscale(0, self.region[1], turtle=turtle)
        self.point(3, '(%d, %d)' % (0, self.region[1]), turtle=turtle)
        self.gotoscale(0, 0, turtle=turtle)
        self.point(3, '(%d, %d)' % (0, 0), turtle=turtle)
        turtle.pu()
    
    def make_grid(self, turtle=turtle):
        turtle.color('#AAAAAA')
        for i in range(1,math.ceil(self.region[0]/self.tile_size)):
            self.gotoscale(i*self.tile_size, 0, turtle=turtle)
            turtle.pd()
            self.gotoscale(i*self.tile_size, self.region[1], turtle=turtle)
            turtle.pu()
        for i in range(1,math.ceil(self.region[1]/self.tile_size)):
            self.gotoscale(0, i*self.tile_size, turtle=turtle)
            turtle.pd()
            self.gotoscale(self.region[0], i*self.tile_size,turtle=turtle)
            turtle.pu()
        turtle.color('#000000')

    def make_walls(self, turtle=turtle):
        for i in self.lines:
            self.drawline(i[0],i[1],i[2],i[3],draw_dots=0,turtle=turtle)
        
    def make_primary_map(self, turtle=turtle):
        for i in allnodes.nodes:
            if (i.ID >= i.IDs-1):
                break
            turtle.pu()
            #print(i.x, i.y)
            self.gotoscale(i.x, i.y, turtle=turtle)
            turtle.pd()
            self.point(3,i.ID,turtle=turtle)
            #turtle.dot(5)
            #turtle.write(i.ID)
            for j in i.nodes:
                if (j >= i.IDs-1):
                    break
                if j > i.ID:
                    #print(j)
                    turtle.color('#AAAAAA')
                    self.gotoscale(allnodes.nodes[j].x, allnodes.nodes[j].y, turtle=turtle)
                    turtle.pd()
                    self.gotoscale(i.x, i.y, turtle=turtle)
                    turtle.pu()
            turtle.pu()
    
    def make_secondary_map(self, turtle=turtle):
        turtle.clear()
        for i in allnodes.nodes:
            if (i.ID >= i.IDs-1):
                turtle.pu()
                #print(i.x, i.y)
                self.gotoscale(i.x, i.y, turtle=turtle)
                turtle.pd()
                self.point(3,i.ID,turtle=turtle)
                #turtle.dot(5)
                #turtle.write(i.ID)
                for j in i.nodes:
                    if j < i.ID:
                        #print(j)
                        turtle.color('#AAAAAA')
                        self.gotoscale(allnodes.nodes[j].x, allnodes.nodes[j].y, turtle=turtle)
                        turtle.pd()
                        self.gotoscale(i.x, i.y, turtle=turtle)
                        turtle.pu()
                turtle.pu()
    
    def make_map(self, turtle=turtle):
        for i in allnodes.nodes:
            turtle.pu()
            #print(i.x, i.y)
            self.gotoscale(i.x, i.y, turtle=turtle)
            turtle.pd()
            self.point(3,i.ID,turtle=turtle)
            #turtle.dot(5)
            #turtle.write(i.ID)
            for j in i.nodes:
                if j > i.ID:
                    #print(j)
                    turtle.color('#AAAAAA')
                    self.gotoscale(allnodes.nodes[j].x, allnodes.nodes[j].y, turtle=turtle)
                    turtle.pd()
                    self.gotoscale(i.x, i.y, turtle=turtle)
                    turtle.pu()
            turtle.pu()
    
    def make_error_map(self, turtle=turtle):
        turtle.clear
        turtle.pu()
        for i in allnodes.nodes:
            self.rx, self.ry = i.x, i.y
            self.measure_tx_toa(animate=0)
            self.locate()
            self.draw_location()
            turtle.pd()
            self.gotoscale(i.x, i.y, turtle=turtle)
            self.point(3,i.ID,turtle=turtle)
            turtle.pu()
    
    def make_mark_map(self, turtle=turtle):
        turtle.clear
        turtle.pu()
        for i in allnodes.nodes:
            self.gotoscale(i.x, i.y, turtle=turtle)
            self.point(3,'%d' % i.tweight,turtle=turtle)

            turtle.pu()
    
    def update_cells(self):
        for i in range(len(self.cell_turtles)):
            self.small_cells[i] = self.fromscale(self.cell_turtles[i].xcor(), self.cell_turtles[i].ycor())
            wireless.ue[i].x = self.small_cells[i][0]
            wireless.ue[i].y = self.small_cells[i][1]
    
    def place_cells(self, color='#000000', turtle=turtle):
        #turtle.color(color)
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        #print('Small Cells:')
        self.cell_turtles = []
        for i in range(len(self.small_cells)):
            self.gotoscale(self.small_cells[i][0], self.small_cells[i][1], turtle=turtle)
            self.cell_turtles.append(turtle.clone())
            self.cell_turtles[-1].st()
            self.cell_turtles[-1].color(color)
            self.cell_turtles[-1].shape('circle')
            self.cell_turtles[-1].ondrag(self.cell_turtles[-1].goto)
            self.cell_turtles[-1].onrelease(self.cell_reload)
            #F = self.point(3, letters`[i], self.small_cells[i][0], self.small_cells[i][1], color, turtle)
            wireless.ue[i].x = self.small_cells[i][0]
            wireless.ue[i].y = self.small_cells[i][1]
        
################################VISUAL FUNCTIONS############################
    
    #setup
    def turtle_setup(self):
        #turtle.setup(0.9, 0.9, 0, 0)
        #turtle.setup(1.0, 1.0, 0, 0)
        turtle.title("Final Year Project")

    def create_clones(self):
        #turtle.pu()
        turtle.speed(0)
        #turtle.speed(1)
        turtle.pu()
        turtle.ht()
        turtle.ondrag(turtle.goto)
        turtle.onrelease(self.pos_reload)
        
        #create a clone for drawing the circles
        self.workings = turtle.clone()
        self.background = turtle.clone()
        self.map = turtle.clone()
        turtle.st()
        self.target = turtle.clone()
        self.target.color('#00FF00')
        self.target.shape('circle')
        self.target.ondrag(self.target.goto)
        self.target.onrelease(self.target_reload)
        self.place_cells('#DC143C',  self.background)
        self.gotoscale(self.tx, self.ty, self.target)
        self.gotoscale(self.rx, self.ry)
    
    def screen_reload(self):
        #Window is not same scale as units used. Need a scale factor
        temp_width, temp_height = self.size_window()
        #reset screen if window size has changed
        if ((self.wwidth != temp_width)& (self.wheight != temp_height)):
            self.wwidth, self.wheight = temp_width, temp_height
            self.get_scale()
            turtle.clearscreen()
            self.create_clones()
            
            #Start drawing
            #self.make_grid(self.background)
            self.make_walls(self.background)
            self.make_box(self.background)
            self.make_primary_map(self.background)
            #self.make_map(self.map)
            #self.make_error_map(self.workings)
            turtle.color('#0000FF')

    def circle(self, x, y, r, turtle=turtle):
        self.gotoscale(x, y-r, turtle=turtle)
        turtle.pd()
        turtle.circle(r*self.scale[2],360)
        turtle.pu()
    
    def draw_circles(self):
        self.workings.clear()
        self.workings.color('#0000FF')
        for i in range(len(self.small_cells)):
            #print(i)
            #print(small_cells[i])
            #print(distances[i])
            self.circle(self.small_cells[i][0], self.small_cells[i][1], self.distances[i], turtle=self.workings)
    
    def draw_intersections(self):
        for i in range(len(self.intersections)):
            for j in range(len(self.intersections[i])):
                self.gotoscale(self.intersections[i][j][0], self.intersections[i][j][1], turtle=self.workings)
                self.point(3, i*2+j, self.intersections[i][j][0], self.intersections[i][j][1], '#FF00FF', turtle=self.workings)
        #for i in range(len(self.intersections)):
            """
            try:
                gotoscale(intersections[i][0], intersections[i][1], scale)
                point(3, letters[i], intersections[i][0], intersections[i][1])
                #point(1, 'x')
            except:
                1
            """
            #self.gotoscale(self.intersections[i][0], self.intersections[i][1], turtle=self.workings)
            #self.point(3, i, self.intersections[i][0], self.intersections[i][1], '#FF00FF', turtle=self.workings)
    
    def draw_location(self):
        self.gotoscale(self.location[0], self.location[1], turtle=self.workings)
        self.point(2, 'X', self.location[0], self.location[1], '#FF00FF', turtle=self.workings)

    def travel(self, x=0, y=0, turtle=turtle):
            angle = (180+math.degrees(math.atan2(y-self.ry,x-self.rx))-turtle.heading())%360-180
            if (angle != 0):
                turtle.lt(angle)
            turtle.fd(self.scale[2]*pythagoras(x,y,self.rx,self.ry))
            self.rx, self.ry = self.fromscale(turtle.xcor(), turtle.ycor())

    def draw_route(self, distance=0, turtle=turtle):
        turtle.clear()
        self.workings.clear()
        turtle.pd()
        turtle.speed(0)
        self.measure_tx_toa(animate=0)
        self.location = self.locate()
        self.draw_location()
        if (allnodes.nodes[len(allnodes.nodes)-2].marked==1):
            for i in self.path:
                #self.gotoscale(allnodes.nodes[i].x, allnodes.nodes[i].y, turtle=turtle)
                self.travel(allnodes.nodes[i].x, allnodes.nodes[i].y, turtle=turtle)
                self.measure_tx_toa(animate=0)
                self.location = self.locate()
                self.draw_location()
            self.travel(self.tx, self.ty, turtle=turtle)
            self.measure_tx_toa(animate=0)
            self.location = self.locate()
            self.draw_location()
            #self.rx, self.ry = turtle.xcor()/self.scale[2], turtle.ycor()/self.scale[2]
            self.rx, self.ry = self.fromscale(turtle.xcor(), turtle.ycor())
            turtle.speed(0)
        turtle.pu()

    def step_travel(self, x1=0, y1=0, x2=0, y2=0, distance=1, turtle=turtle):
            angle = (180+math.degrees(math.atan2(y2-y1,x2-x1))-turtle.heading())%360-180
            if (angle != 0):
                turtle.lt(angle)
            #turtle.fd(self.scale[2]*pythagoras(x,y,self.rx,self.ry))
            turtle.fd(self.scale[2]*distance)
            self.rx, self.ry = self.fromscale(turtle.xcor(), turtle.ycor())
    
    def draw_step_route(self, turtle=turtle):
        turtle.clear()
        self.workings.clear()
        turtle.pd()
        turtle.speed(0)
        self.measure_tx_toa(animate=0)
        self.location = self.locate()
        self.draw_location()
        if (allnodes.nodes[len(allnodes.nodes)-2].marked==1):
            for i in self.path:
                while pythagoras(allnodes.nodes[i].x,allnodes.nodes[i].y,self.rx,self.ry) > self.tolerance:
                    #self.gotoscale(allnodes.nodes[i].x, allnodes.nodes[i].y, turtle=turtle)
                    self.step_travel(self.rx, self.ry, allnodes.nodes[i].x, allnodes.nodes[i].y, self.step, turtle=turtle)
                    self.reconnect()
                    #self.measure_tx_toa(animate=0)
                    #self.location = self.locate()
                    self.draw_location()
                #self.gotoscale(allnodes.nodes[i].x, allnodes.nodes[i].y, turtle=turtle)
                self.step_travel(self.rx, self.ry, allnodes.nodes[i].x, allnodes.nodes[i].y, pythagoras(allnodes.nodes[i].x,allnodes.nodes[i].y,self.rx,self.ry), turtle=turtle)
                self.reconnect()
                #self.measure_tx_toa(animate=0)
                #self.location = self.locate()
                self.draw_location()
            self.travel(self.tx, self.ty, turtle=turtle)
            self.reconnect()
            #self.measure_tx_toa(animate=0)
            #self.location = self.locate()
            self.draw_location()
            #self.rx, self.ry = turtle.xcor()/self.scale[2], turtle.ycor()/self.scale[2]
            self.rx, self.ry = self.fromscale(turtle.xcor(), turtle.ycor())
            turtle.speed(0)
        turtle.pu()
    
    def draw_local_step_route(self, turtle=turtle):
        turtle.clear()
        self.workings.clear()
        turtle.pd()
        turtle.speed(0)
        self.measure_tx_toa(animate=0)
        self.location = self.locate()
        self.draw_location()
        if (allnodes.nodes[len(allnodes.nodes)-2].marked==1):
            self.path.pop(0)
            for i in self.path:
                while pythagoras(allnodes.nodes[i].x,allnodes.nodes[i].y,self.location[0],self.location[1]) > self.step:
                    #self.gotoscale(allnodes.nodes[i].x, allnodes.nodes[i].y, turtle=turtle)
                    self.step_travel(self.location[0],self.location[1], allnodes.nodes[i].x, allnodes.nodes[i].y, self.step, turtle=turtle)
                    self.reconnect()
                    #self.measure_tx_toa(animate=0)
                    #self.location = self.locate()
                    self.draw_location()
                self.step_travel(self.location[0],self.location[1], allnodes.nodes[i].x, allnodes.nodes[i].y, pythagoras(allnodes.nodes[i].x,allnodes.nodes[i].y,self.location[0],self.location[1]), turtle=turtle)
                self.reconnect()
                #self.measure_tx_toa(animate=0)
                #self.location = self.locate()
                self.draw_location()
            #self.travel(self.tx, self.ty, turtle=turtle)
            #self.measure_tx_toa(animate=0)
            #self.location = self.locate()
            #self.draw_location()
            ##self.rx, self.ry = turtle.xcor()/self.scale[2], turtle.ycor()/self.scale[2]
            #self.rx, self.ry = self.fromscale(turtle.xcor(), turtle.ycor())
            turtle.speed(0)
        turtle.pu()
    
    def drawline(self,x1,y1,x2,y2,draw_dots=0,turtle=turtle):
        self.gotoscale(x1,y1,turtle=turtle)
        turtle.pd()
        self.gotoscale(x2,y2,turtle=turtle)
        turtle.pu()
        
    def draw(self):
        #self.make_map(background)
        self.gotoscale(self.rx, self.ry, turtle=turtle)
        self.draw_circles()
        #self.draw_intersections()
        self.draw_location()
    
    def reload(self):
        #self.measure_plm()
        print('\n')
        print('Recievers')
        for i in self.small_cells:
            print(i)
        #place turtle
        self.gotoscale(self.rx, self.ry, turtle=turtle)
        self.measure_tx_toa(animate=0)
        #self.measure_rx_toa(animate=1)
        #self.locate()
        #self.draw()
        print('Intersection points')
        for i in self.intersections:
            print(i)

        print('Actual Location')
        print(self.rx, self.ry)
        print('Calculated Location')
        print(self.location[0], self.location[1])
        print('Error: ', pythagoras(self.rx,self.ry,self.location[0],self.location[1]))
        self.finished = 1
    
    # When bot gets moved
    def pos_reload(self, x=0, y=0):
        """
        if (self.finished == 1):
            self.finished = 0
            self.update_cells()
            self.screen_reload()
            self.rx, self.ry = self.fromscale(x, y)
            #self.rx, self.ry = x/self.scale, y/self.scale
            self.reload()
        #"""
        #"""
        if (self.finished == 0):
            self.finished = 0
            self.update_cells()
            self.rx, self.ry = self.fromscale(x, y)
            self.screen_reload()
            #allnodes.nodes[len(allnodes.nodes)-2].x = self.rx
            #allnodes.nodes[len(allnodes.nodes)-2].y = self.ry
            self.reconnect()
            #self.measure_tx_toa(animate=0)
            #self.location = self.locate()
            allnodes.nodes[len(allnodes.nodes)-2].x = self.location[0]
            allnodes.nodes[len(allnodes.nodes)-2].y = self.location[1]
            allnodes.detatch(len(allnodes.nodes)-2)
            for i in range(len(allnodes.nodes)):
                allnodes.makelosline(len(allnodes.nodes)-2, i)
            self.make_secondary_map(self.map)
            print('start', len(allnodes.nodes)-2)
            print('end', len(allnodes.nodes)-1)
            print('calculating routes')
            #self.path, xs, ys = allnodes.djikstra(len(allnodes.nodes)-1, len(allnodes.nodes)-2) #Astar would be a better solution here 
            self.path, xs, ys = allnodes.astar(len(allnodes.nodes)-1, len(allnodes.nodes)-2) #could be improved by starting at both ends and finding route where they meet
            #self.draw_route()
            #self.draw_step_route()
            self.draw_local_step_route()
            #self.reload()
        #"""
    
    # Randomly move bot
    def move_reload(self):
        self.screen_reload()
        self.move_target()
        self.reload()
    
    # When reciever gets moved
    def cell_reload(self, x=0, y=0):
        if (self.finished == 1):
            self.finished = 0
            self.update_cells()
            #self.move_reload()

    # When home/target/goal gets moved
    def target_reload(self, x=0, y=0):
        if (self.finished == 0):
            self.finished = 0
            self.update_cells()
            self.rx, self.ry = self.fromscale(turtle.xcor(), turtle.ycor())
            self.tx, self.ty = self.fromscale(x, y)
            #allnodes.nodes[len(allnodes.nodes)-2].x = self.rx
            #allnodes.nodes[len(allnodes.nodes)-2].y = self.ry
            self.reconnect()
            #self.measure_tx_toa(animate=0)
            #self.location = self.locate()
            allnodes.nodes[len(allnodes.nodes)-2].x = self.location[0]
            allnodes.nodes[len(allnodes.nodes)-2].y = self.location[1]
            allnodes.nodes[len(allnodes.nodes)-1].x = self.tx
            allnodes.nodes[len(allnodes.nodes)-1].y = self.ty
            allnodes.detatch(len(allnodes.nodes)-2)
            allnodes.detatch(len(allnodes.nodes)-1)
            for i in range(len(allnodes.nodes)-1):
                allnodes.makelosline(len(allnodes.nodes)-2, i)
                allnodes.makelosline(len(allnodes.nodes)-1, i)
            #self.reload()
            #wireless.Printer.drawNetwork(fillMethod="SINR", filename="sinrMap", obstacleVector = wireless.obstacles)
            #self.screen_reload()
            #wireless.Printer.drawNetwork(fillMethod="SINR", filename="sinrMap", obstacleVector = wireless.obstacles)
            self.make_secondary_map(self.map)
            print('done printing')
            print('start', len(allnodes.nodes)-2)
            print('end', len(allnodes.nodes)-1)
            print('calculating routes')
            #self.path, xs, ys = allnodes.djikstra(len(allnodes.nodes)-1, len(allnodes.nodes)-2) #Astar would be a better solution here
            self.path, xs, ys = allnodes.astar(len(allnodes.nodes)-1, len(allnodes.nodes)-2) #could be improved by starting at both ends and finding route where they meet
            #self.draw_route()
            #self.draw_step_route()
            self.draw_local_step_route()
            #self.make_mark_map(turtle=self.workings)
