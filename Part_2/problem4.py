import argparse
import matplotlib.pyplot as plt
from celluloid import Camera
from grid import Grid

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Name of scenario file.")
    args = parser.parse_args()
    print(args.filename)
    g = Grid(0,0)
    g.process_file(args.filename)
    #g.print_grid()
    g.save_grid("results/problem4A")

    fig = plt.figure()
    camera = Camera(fig)
    current = g.pedestrians[0]
    result = g.path_movement_dijkstra(current)
    print(result)
    for i in result:
        g.change_ped_state(current, i)
        g.draw_grid()
        camera.snap()
        current = i
        g.pedesnum = 0
    animation = camera.animate()
    animation.save('results/problem4.gif', writer = 'imagemagick')
    g.save_grid("results/problem4B")