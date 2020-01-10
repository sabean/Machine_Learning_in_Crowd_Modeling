import argparse
from grid import Grid

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Name of scenario file.")
    args = parser.parse_args()
    g = Grid(0,0)
    g.process_file(args.filename)
    g.save_grid("results/problem2A")
    for i in g.pedestrians:
        result = g.path_movement(i)
    print(result)
    g.save_grid("results/problem2B")
    g.print_steps()