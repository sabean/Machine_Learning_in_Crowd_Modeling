import argparse
import matplotlib.pyplot as plt
from celluloid import Camera
from grid import Grid

if __name__ == '__main__':
    g = Grid(5,100)
    g.set_pedestrians([(0,0)])
    g.set_target((4,99))

    fig = plt.figure()
    camera = Camera(fig)
    current = g.pedestrians[0]
    initial = current
    g.save_grid("results/test1A")

    result = g.path_movement_dijkstra(current)
    for i in result:
        g.change_ped_state(current, i)
        g.draw_grid()
        camera.snap()
        current = i
        g.pedesnum=0
    animation = camera.animate()
    animation.save('results/test1.gif', writer = 'imagemagick')
    g.save_grid("results/test1B")
    print("Number of steps: ")
    dsteps = g.print_steps()
    steps = dsteps[initial]
    print("Estimated time of travel: ")
    print((steps*0.4)/1.33)
