#import turtle
#import math
from pyltes.network import CellularNetwork

################################CALCULATION FUNCTIONS############################

def pythagoras(a,b,c=0,d=0):
    return ((a-c)**2+(b-d)**2)**0.5

def inverse2x2(a):
    det = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return [[a[1][1]/det, -a[0][1]/det], [-a[1][0]/det, a[0][0]/det]]

def mmult(inverse, consts):
    x = inverse[0][0]*consts[0]+inverse[0][1]*consts[1]
    y = inverse[1][0]*consts[0]+inverse[1][1]*consts[1]
    return [x, y]

def sign(x):
    if (x == 0):
        return 0
    return x/abs(x)

def doublecircle(x1,y1,r1,x2,y2,r2):
    #Returns intersection points of 2 circles for 2d
    #For 3d require doing intersections with spheres
    q = pythagoras(x2-x1, y2-y1)
    x3 = (x1+x2)/2+(x2-x1)*(r1**2-(r2**2))/(2*q**2)-(y2-y1)*(((r1+r2)**2-q**2)*(q**2-(r1-r2)**2))**0.5/(2*q**2)
    y3 = (y1+y2)/2+(y2-y1)*(r1**2-(r2**2))/(2*q**2)+(x2-x1)*(((r1+r2)**2-q**2)*(q**2-(r1-r2)**2))**0.5/(2*q**2)
    x4 = (x1+x2)/2+(x2-x1)*(r1**2-(r2**2))/(2*q**2)+(y2-y1)*(((r1+r2)**2-q**2)*(q**2-(r1-r2)**2))**0.5/(2*q**2)
    y4 = (y1+y2)/2+(y2-y1)*(r1**2-(r2**2))/(2*q**2)-(x2-x1)*(((r1+r2)**2-q**2)*(q**2-(r1-r2)**2))**0.5/(2*q**2)
    return [[x3, y3], [x4, y4]]

def distance2w(d,ptx=30,gamma=20,xg=0,d0=1,L0=1):
    #Used for simulation to get expected value for power
    return ptx/(10**((10*gamma*math.log10(d/d0)+L0+xg)/10))

def w2distance(prx,ptx=30,gamma=20,xg=0,d0=1,L0=1):
    return d0*10**((10*math.log10(ptx/prx)-xg-L0)/(10*gamma))

def time2distance(time, c=330):
    #using speed of sound because it's just a number
    return time*c

def coords2index(x,y, region, tile_size=1):
    output = int(((x)/tile_size)+int((y)/tile_size)*(math.ceil(region[0]/tile_size))) #centred origin
    return int(((x)/tile_size)+int((y)/tile_size)*(math.ceil(region[0]/tile_size))) #centred origin

def calculateDistance(SINR=0,pSend=0):
    pRec = calculatepRec(SINR)
    #distance = calculateDistance(sum_power_mw, pSend)
    lambda_val = 0.345383
    a = 4.0
    b = 0.0065
    c = 17.1
    d = 10.8
    s = 15.8

    ht = 40
    hr = 1.5
    f = 2.1
    gamma = a - b*ht + c/ht
    Xf = 6 * math.log10( f/2 )
    Xh = -d * math.log10( hr/2 )

    R0 = 100.0
    R0p = R0 * pow(10.0,-( (Xf+Xh) / (10*gamma) ))

    alpha = 20 * math.log10( (4*math.pi*R0p) / lambda_val )
    
    distance = R0*10**((pSend-pRec-alpha-Xf-Xh-s)/(10*gamma))
    if (distance<R0p):
        distance = lambda_val*10**((pSend-pRec-s)/20)/(4*math.pi)
    return distance

def calculateNoise(bandwidth=20):
    k = 1.3806488 * math.pow(10, -23)
    T = 293.0
    BW = bandwidth * 1000 * 1000
    N = 10*math.log10(k*T) + 10*math.log10(BW)
    return N

def calculatepRec(SINR):
    # SINR = Signal to (Interference + Noise) Ratio
    # One base statioin means no interference. That leaves noise to deal with
    SINR_mw = 10**(SINR/10)

    N_mw = math.pow(10, calculateNoise()/10)
    S_mw = SINR_mw*N_mw
    
    receivedPower_connectedBS = 10*math.log10(S_mw)
    pRec = receivedPower_connectedBS
    #receivedPower_otherBS_mw = I_mw
    #receivedPower_one = math.log10(receivedPower_otherBS_mw)
    #pRec = receivedPower_one
    #sum_power_mw = 2.0*10**(receivedPower_one/10.0)
    #pRec = 10*math.log10(sum_power_mw)
    #pRec = SINR*10**math.log10(abs(SINR))
    #print("Estimates:", SINR, pRec)
    return pRec


from pathfinding import *

region = [2000, 2000]
small_cells=[
    [0, 0],
    [0, 2000],
    [2000, 1000],
]

c = 299792458
#c = 330
#sample rate
s_r = 800000000

rawlines = [
    #[0, 0, 0, 20, 5],
    #[0, 20, 20, 20, 5],
    #[20, 20,20, 0, 5],
    #[20, 0, 0, 0, 5],
    
    #[9.5, 12, 15, 8, 5],
    #[10.5, 8, 5, 12, 5],
    #[10.5, 12, 5, 8, 5],
    #[12, 10.5, 8, 5, 5],
    
    #[14.5, 17, 17, 13, 5],
    #[15.5, 13, 10, 17, 5],
    #[15.5, 17, 10, 13, 5],
    #[17, 15.5, 13, 10, 5],

    [400, 1000, 1600, 1000, 0.01],
    [1000, 400, 1000, 1600, 0.01],
    [600, 700, 600, 1300, 0.01],
    [1500, 1000, 1500, 1150, 0.01],
    [1300, 800, 1300, 1300, 0.01],
    [800, 1000, 800, 700, 0.01],
    [1100, 800, 1600, 800, 0.01],
    
    #[950, 1200, 1500, 800, 0.02],
    #[1050, 800, 500, 1200, 0.02],
    #[1050, 1200, 500, 800, 0.02],
    #[1200, 1050, 800, 500, 0.02],
    
    [1650, 1900, 1900, 1500, 0.01],
    [1750, 1500, 1200, 1900, 0.01],
    [1750, 1900, 1200, 1500, 0.01],
    [1900, 1750, 1500, 1200, 0.01],
    
    #[400, 100, 1600, 1300, 1],
    #[1600, 100, 400, 1300, 1],
]

wireless = CellularNetwork()
wireless.Generator.create1BSnetwork(max(region[0], region[1])/(2*3**0.5)) # Creates a base station with a radius of 1666. idk units, probably up to your own scale
wireless.Generator.insertUErandomly(3) # Creates 20 end users in random locations

for i in rawlines:
    wireless.obstacles.append(i)
#print(wireless.obstacles == rawlines)
#wireless.obstacles == rawlines

wireless.connectUsersToTheBestBS(wireless.obstacles) # devices.py

#wireless.Printer.drawHistogramOfUEThroughput("thrHistogram")
#wireless.Printer.drawNetwork(fillMethod="SINR", filename="sinrMap", obstacleVector = wireless.obstacles)
#print("done printing")

width = 20
tolerance = 15
step = 50

allnodes = network()
allnodes.generate_nodes(rawlines, width, tolerance)

#allnodes.info()

from model import *

home = model(region, rawlines, small_cells, c, s_r, step, tolerance)
home.screen_reload()
