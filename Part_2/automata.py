# States := {E : empty(white), P: pedistrian(red), O: obstacle(blue), T:target(yellow), M: path, move(pink)}
# blue=0 yellow=0.6 red=0.7 pink=0.95 white=1

class Automata:
    def __init__(self, cell_type, pos):
        self.type = cell_type   #cell type E,P,O,T or M
        self.side = 40         #length initially 40
        self.steps = 0
        self.pos = pos          
        self.dict_code = {'E':1, 'P':0.7, 'O':0, 'T':0.6, 'M': 0.95}
        self.value = self.dict_code[self.type]
        if self.type == 'P':    #if the automata is active to move
            self.active = 1
        else:
            self.active = 0

    def change_value(self):
        self.value = self.dict_code[self.type]
        if self.type == 'P':
            self.active = 1
        else:
            self.active = 0
        
    def neighbors(self, num):
        u = self.pos[0]
        v = self.pos[1]
        if num == 4:
            return [(u,v+1), (u+1,v), (u,v-1), (u-1,v)]
        else:
            return [(u-1, v+1),(u, v+1), (u+1,v+1), (u+1,v), (u+1, v-1), (u, v-1), (u-1, v-1), (u-1,v)]
    
    def print_automata(self):
        print("------------------")
        print("| Type: {0}        {1}".format(self.type, '|'))
        print("| Position:{0}{1}".format(self.pos, '|'))
        print("------------------")

    def print_short(self):
        print('  {0}  '.format(self.type), end="")