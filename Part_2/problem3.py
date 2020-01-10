import argparse
import matplotlib.pyplot as plt
from celluloid import Camera
from grid import Grid

if __name__ == '__main__':
    g = Grid(50,50)
    g.set_target((25,25))
    g.set_pedestrians([(48, 24), (31, 47), (5, 38), (5, 10), (31, 1)])
    g.save_grid("results/problem3A")

    fig = plt.figure()
    camera = Camera(fig)
    while True:
        current_peds = []
        for x in g.pedestrians:
            current_peds.append(x)
        for i in current_peds:
            g.move_one(i)
        g.pedesnum = 0
        g.draw_grid()
        camera.snap()
        if g.check_active() == 0:
            break
    animation = camera.animate()
    animation.save('results/problem3.gif', writer = 'imagemagick')
    g.save_grid("results/problem3B")

    for i in g.trace:
        print(i)
        print(len(i))
        print()
    