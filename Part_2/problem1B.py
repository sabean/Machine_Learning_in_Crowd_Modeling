import argparse
from grid import Grid

if __name__ == '__main__':
    # Reading Scenarios from file
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Name of scenario file.")
    args = parser.parse_args()
    print(args.filename)
    g = Grid(0,0)
    g.process_file(args.filename)

    # This function moves the pedestrian according to closeness with target.
    g.save_grid("results/problem1B1")
    current_pos = g.pedestrians[0]
    g.move_one(current_pos)
    g.save_grid("results/problem1B2")