import numpy as np
import math
import queue
import ast
import matplotlib.pyplot as plt
from automata import Automata
from celluloid import Camera
from collections import defaultdict

class Grid:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.target = ()
        self.pedestrians = []
        self.obstacles = []
        self.trace = []     #path of the automata moved to reach the target
        self.pedesnum = 0      #like counter for different pedestrians
        lst = []
        for i in range(self.length):
            temp = []
            for j in range(self.width):
                temp.append(Automata('E',(i,j)))
            lst.append(temp)
        self.cellular_grid = np.array(lst)

    def init_trace(self):
        for i in self.pedestrians:
            self.trace.append([i])

    def create_grid(self):
        lst = []
        for i in range(self.length):
            temp = []
            for j in range(self.width):
                temp.append(Automata('E',(i,j)))
            lst.append(temp)
        self.cellular_grid = np.array(lst)

    def change_celltype(self, pos, ctype):
        self.cellular_grid[pos[0], pos[1]].type = ctype
        self.cellular_grid[pos[0], pos[1]].change_value()

    def new_celltype(self, pos, ctype):
        self.cellular_grid[pos[0], pos[1]].type = ctype
        self.cellular_grid[pos[0], pos[1]].change_value()
        if ctype == 'P':
            self.pedestrians.append(pos)
        if ctype == 'O':
            self.obstacles.append(pos)
    
    def deactivate_auto(self, pos):
        self.cellular_grid[pos[0], pos[1]].active = 0
    
    def is_active(self, pos):
        if self.cellular_grid[pos[0], pos[1]].active == 1:
            return 1
        return 0

    def check_pedestrian(self, pos):
        if pos in self.pedestrians:
            return True
        else:
            return False

    def path_movement(self, pedpos, numNeighbors=4):
        currpos = pedpos
        count = 0
        path = []
        while(currpos != self.target):
            count+=1
            dist_lst = []
            path.append(currpos)
            for i in self.computeNeighbors(currpos, numNeighbors):
                dist_lst.append((self.dist(i), i))
            distances = sorted(dist_lst, key=lambda tup: tup[0])
            self.change_ped_state(currpos, distances[0][1])
            currpos = distances[0][1]
            self.pedesnum = 0
            if count > 100:
                break
        #path.append(self.target)
        return path, count
    
    def path_movement_dijkstra(self, init, numNeighbors=4):
        visited_nodes, possibility = self.computeDijkstra(init, numNeighbors)
        constructed_path = []
        if possibility:
            constructed_path = self.construct_path(init, visited_nodes)
        return constructed_path


    def construct_path(self, init, visited):
        curr = self.target
        path = []
        while(curr != init):
            path.append(curr)
            curr = visited[curr]
        path.append(init) 
        path.reverse() 
        return path
    
    def computeDijkstra(self, init, numNeighbors=4):
        temp = queue.PriorityQueue()
        temp.put(init, 0)
        visited = {}
        cumulativeCost = {}
        visited[init] = None
        cumulativeCost[init] = 0
        while not temp.empty():
            current_node = temp.get()
            if(current_node == self.target):
                return visited, True
            neighbor = self.computeNeighbors(current_node, numNeighbors)

            for values in neighbor:
                new_cost = cumulativeCost[current_node] + self.cost_value(values, current_node)
                if values not in cumulativeCost or new_cost < cumulativeCost[values]:
                    cumulativeCost[values] = new_cost
                    temp.put(values,new_cost)
                    visited[values] = current_node
        return "No path found!", False

    def costDir(self, coordinate1, coordinate2):
        sideways = [(0,1), (0, -1)]
        up_down = [(1, 0), (-1, 0)]
        diagonal = [(1, 1), (-1, -1),(1, -1), (-1, 1)]
        res = (coordinate1[0] - coordinate2[0], coordinate1[1] - coordinate2[1])
        if res in up_down:
            return 1
        if res in sideways:
            return 1
        if res in diagonal:
            return math.sqrt(2)

    def dist(self, pedpos):
        return math.sqrt(pow(pedpos[0]-self.target[0], 2) + pow(pedpos[1]-self.target[1], 2))

    def cost(self, r):
        d1 = self.dist(r)
        d2 = self.dist(self.target)
        if d1 < d2:
            return math.exp(1/(d1**2 - d2**2))
        else:
            return 0


    def cost_value(self, pedpos, current):
        sumcost = 0
        for i in self.pedestrians:
            if i != current:
                if i != pedpos:
                    sumcost += self.cost(pedpos)
        return sumcost


    def change_cellvalue(self, pos, value):
        self.cellular_grid[pos[0], pos[1]].value = value

    def boundaryCheck(self, val):
        (x, y) = val
        return 0 <= x < self.length and 0 <= y < self.width
    
    def computeNeighbors(self,coord, numNeighbors=4):
        (x, y) = coord
        if numNeighbors == 8:
            neighbors = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1)]
        else:
            neighbors = [(x-1, y),(x, y+1), (x+1, y),(x, y-1)]
        validNeighbors = []
        for i in neighbors:
            if(self.boundaryCheck(i)):
                validNeighbors.append(i)
        result_neighbors = []
        for j in validNeighbors:
            if j not in self.obstacles:
                if j not in self.pedestrians:
                    result_neighbors.append(j)
        return result_neighbors  
    
    
    def set_target(self, pos):
        self.target = pos
        self.change_celltype(pos, 'T')

    def set_pedestrians(self, lst):
        self.pedestrians = lst
        self.init_trace()
        for i in lst:
            self.change_celltype(i, 'P')

    def set_obstacles(self, lst):
        self.obstacles = lst
        for i in lst:
            self.change_celltype(i, 'O')
    
    def print_steps(self):
        dict1 = {}
        for i in self.trace:
            self.cellular_grid[i[0][0], i[0][1]].steps = len(i)
            print(i[0], '  => ', self.cellular_grid[i[0][0], i[0][1]].steps, ' steps')
            dict1[i[0]] = self.cellular_grid[i[0][0], i[0][1]].steps
        return dict1

    def get_cellarray(self):
        lst1 = []
        for i in range(self.length):
            lst2 = []
            for j in range(self.width):
                lst2.append(self.cellular_grid[i, j].value)
            lst1.append(lst2)
        return np.array(lst1)

    def get_target(self):
        return self.target

    def get_pedestrians(self):
        return self.pedestrians

    def get_obstacles(self):
        return self.obstacles

    def print_grid(self):
        for i in range(self.length):
            for j in range(self.width):
                self.cellular_grid[i, j].print_short()
            print()
    
    def process_file(self, filename):
        with open(filename) as f:
            content = f.readlines()
            for i in content:
                line = i.rstrip()
                line = line.split(': ')
                if line[0] == 'length':
                    self.length = int(line[1])
                elif line[0] == 'width':
                    self.width = int(line[1])
                    self.create_grid()
                elif line[0] == 'target':
                    self.set_target(ast.literal_eval(line[1]))
                elif line[0] == 'pedestrians':
                    self.set_pedestrians(ast.literal_eval(line[1]))
                elif line[0] == 'obstacles':
                    self.set_obstacles(ast.literal_eval(line[1]))

    def cost_path_movement(self, pedpos, computeNeighbors=4):
        currpos = pedpos
        count = 0
        path = []
        while(currpos != self.target):
            count+=1
            dist_lst = []
            path.append(currpos)
            for i in self.computeNeighbors(currpos, computeNeighbors):
                dist_lst.append((self.cost_value(i, currpos)+self.dist(i), i))
            distances = sorted(dist_lst, key=lambda tup: tup[0])
            currpos = distances[0][1]
            if count > 70:
                break
        return path, count

    def tester_block(self, lst):
        for i in lst:
            if self.check_pedestrian(i) == False:
                return 0
        return 1

    def tester_corner(self, lst):
        if lst[0] != self.target:
            return 0
        if self.check_pedestrian(lst[1]) != True:
            return 0
        if self.check_pedestrian(lst[2]) != True:
            return 0
        return 1

    def block_Test(self, pos):
        (x,y) = pos
        EN = {1:(x-1, y-1), 2:(x-1, y), 3:(x-1, y+1), 4:(x, y+1), \
            5:(x+1, y+1), 6:(x+1, y), 7:(x+1, y-1), 8:(x, y-1)}
        hor1 = [EN[1],EN[2],EN[3]]
        hor2 = [EN[7], EN[6], EN[5]]
        vert1 = [EN[3],EN[4], EN[5]]
        vert2 = [EN[1], EN[8], EN[7]]
        pack1 = [hor1, hor2, vert1, vert2]
        count = 0
        for i in pack1:
            result = self.tester_block(i)
            if result == 1:
                count += 1
        if count > 1:
            return 1
        return 0

    def corner_Test(self, pos):
        (x,y) = pos
        EN = {1:(x-1, y-1), 2:(x-1, y), 3:(x-1, y+1), 4:(x, y+1), \
            5:(x+1, y+1), 6:(x+1, y), 7:(x+1, y-1), 8:(x, y-1)}
        corner1 = [EN[1],EN[2], EN[8]]
        corner2 = [EN[3],EN[2], EN[4]]
        corner3 = [EN[5],EN[4], EN[6]]
        corner4 = [EN[7],EN[6], EN[8]]
        pack2 = [corner1, corner2, corner3, corner4]
        count = 0
        for i in pack2:
            result = self.tester_corner(i)
            if result == 1:
                count += 1
        if count > 0:
            return 1
        return 0
        

    def change_ped_state(self, before, now):
        if now == self.target:
            self.deactivate_auto(before)
        elif before == now:
            self.deactivate_auto(before)
        else:
            if self.block_Test(before) == 0 and self.corner_Test(before) == 0:
                self.new_celltype(now, 'P')
                self.new_celltype(before, 'M')
                self.pedestrians.remove(before)
                self.trace[self.pedesnum].append(now)
                self.pedesnum += 1
            else:
                self.deactivate_auto(before)
    
    def check_active(self):
        count = 0
        for i in self.pedestrians:
            if self.is_active(i):
                count += 1
        if count > 0:
            return 1
        return 0

    def move_one(self, currpos, numNeighbors=4):
        dist_lst = []
        for i in self.computeNeighbors(currpos, numNeighbors):
            dist_lst.append((self.dist(i) + self.cost_value(i, currpos), i))
        distances = sorted(dist_lst, key=lambda tup: tup[0])
        newpos = distances[0][1]
        self.change_ped_state(currpos, newpos)
    
    def draw_grid(self):
        canvas =  self.get_cellarray()
        data = np.flip(canvas, 0)
        plt.pcolor(data, cmap= 'gist_ncar', edgecolors='k', linewidth=1, vmin=0, vmax=1)
        ax = plt.gca()
        ax.set_aspect('equal')
        empty_string_labels_x = ['']*self.length
        empty_string_labels_y = ['']*self.width
        ax.set_xticklabels(empty_string_labels_x)
        ax.set_yticklabels(empty_string_labels_y)
        ax.tick_params(axis=u'both', which=u'both',length=0)

    def save_grid(self, name):
        canvas =  self.get_cellarray()
        data = np.flip(canvas, 0)
        plt.pcolor(data, cmap= 'gist_ncar', edgecolors='k', linewidth=1, vmin=0, vmax=1)
        ax = plt.gca()
        ax.set_aspect('equal')
        empty_string_labels_x = ['']*self.length
        empty_string_labels_y = ['']*self.width
        ax.set_xticklabels(empty_string_labels_x)
        ax.set_yticklabels(empty_string_labels_y)
        ax.tick_params(axis=u'both', which=u'both',length=0)
        newname = name+'.png'
        plt.savefig(newname)