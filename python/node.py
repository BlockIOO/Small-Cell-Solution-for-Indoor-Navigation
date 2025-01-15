class node:
    IDs = -1

    def __init__(self, x=0, y=0):
        self.nodes = [] #neighbouring nodes
        self.weights = []
        self.marked = 0
        self.origin = -1 #node used to reach, -1 means origin
        node.IDs += 1
        self.ID = node.IDs
        self.x = x
        self.y = y
        self.tweight = 0

    def num(self, n):
        self.ID = n
        
    def add_node(self, n, d=1):
        self.nodes.append(n)
        self.weights.append(d)

    def setog(self, n):
        self.origin = n
        
    def mark(self, weight=0):
        self.marked = 1
        self.tweight = weight
    
    def reset(self):
        self.marked = 0
        self.origin = -1
        self.tweight = 0
    
    def info(self):
        print("ID: %d\nLocation: %f, %f\nOrigin: %d\nMarked: %d\nNeighbours:" % (self.ID, self.x, self.y, self.origin, self.marked))
        print(self.nodes)
        print(self.weights)
        #for i in range(len(self.nodes)):
        #    print(self.nodes[i], self.weights[i])
        print("")
