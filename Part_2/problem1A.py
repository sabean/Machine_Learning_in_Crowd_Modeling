import tkinter as tk
from grid import Grid

class Application(tk.Frame):

    def __init__(self, master, pos, txt, auto):
        super(Application, self).__init__(master)
        self.grid(row=pos[0], column=pos[1], sticky='nswe')
        self.value = txt
        self.color_dict = {' ' : 'white', 'P': 'red', 'O': 'blue', 'T': 'yellow', 'M':'pink'}
        self.create_widget(pos)
        self.automata = auto

    def create_widget(self, pos):
        self.bttn = tk.Button(self)
        self.bttn['fg'] = 'black'
        self.bttn['relief'] = 'solid'
        self.bttn['text'] = self.value
        self.bttn['bg'] = self.color_dict[self.value]
        self.bttn['activebackground'] = self.color_dict[self.value]
        self.bttn['command'] = self.update_text
        self.bttn.grid(row=pos[0], column=pos[1], sticky='nswe')

    def update_text(self):
        if self.value == ' ':
            self.value = 'P'
            self.automata.type = 'P'
            
        elif self.value == 'P':
            self.value = 'O'
            self.automata.type = 'O'

        elif self.value == 'O':
            self.value = 'T'
            self.automata.type = 'T'

        elif self.value == 'T':
            self.value = ' '
            self.automata.type = 'E'

        self.bttn['text'] = self.value
        self.bttn['bg'] = self.color_dict[self.value]
        self.bttn['activebackground'] = self.color_dict[self.value]


def GUI(root, g):
    length = g.length
    width = g.width
    for i in range(length):
        for j in range(width):
            auto = g.cellular_grid[i, j]
            txt = ' ' if auto.type=='E' else auto.type
            L = Application(root, (i,j), txt, auto)


if __name__ == "__main__":
    g = Grid(5,5)
    g.change_celltype((0,0), 'O') # Adding Obstacles in cells
    g.change_celltype((1,1), 'T') # Adding Targets in cells
    g.change_celltype((2,2), 'P') # Adding Pedestrian in cells
    root = tk.Tk()
    mainarea = tk.Frame(root)
    mainarea.pack(expand=True, fill='both', side='right')
    
    GUI(mainarea, g)
    root.mainloop()
    g.print_grid()
