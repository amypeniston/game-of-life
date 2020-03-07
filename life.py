import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse
from seeds import SEEDS


def generation(universe):
    """
        Create one iteration of the Game of Life.

        Parameters
        ----------
        universe: numpy.ndarray
            A 2D matrix representing the current state of the universe.
    """

    new_universe = np.copy(universe)

    for y in range(universe.shape[0]):
        for x in range(universe.shape[1]):
            new_universe[y, x] = apply_rules(x, y, universe)
    return new_universe


def apply_rules(x, y, universe):
    """
        Determine survival for a specific cell using Conway's original rules.
        Calculations simulate an infinite universe via toroidal boundary conditions (cells wrap around the screen).

        Parameters
        ----------
        universe: numpy.ndarray
            A 2D matrix representing the current state of the universe.
        x: int
            Horizontal cell position.
        y: int
            Vertical cell position.
    """
    
    # Get universe size for toroidal boundary condition math
    ny = universe.shape[0]
    nx = universe.shape[1]

    # Count 8 surrounding cells
    num_neighbors = int((universe[y, (x - 1) % nx] + universe[y, (x + 1) % nx] + 
                         universe[(y - 1) % ny, x] + universe[(y + 1) % ny, x] + 
                         universe[(y - 1) % ny, (x - 1) % nx] + universe[(y - 1) % ny, (x + 1) % nx] + 
                         universe[(y + 1) % ny, (x - 1) % nx] + universe[(y + 1) % ny, (x + 1) % nx]))

    # Apply rules
    if universe[y, x] and not 2 <= num_neighbors <= 3:
        return 0
    elif num_neighbors == 3:
        return 1
    return universe[y, x]


def place_seed(universe, seed, pos):
    """
        Places a seed array at the desired position within the universe.

        Parameters
        ----------
        universe: numpy.ndarray
            A 2D matrix representing the current state of the universe.
        seed: str
            Human friendly name for a seed array.
        pos: tuple
            Tuple of integers representing seed destination (x, y) coordinates.
    """

    # Explicitly name x and y coordinates, for clarity
    x_pos, y_pos = pos

    # Get universe size for toroidal boundary condition math
    nx = universe.shape[1]
    ny = universe.shape[0]

    # Determine where to place top left corner of seed
    i = x_pos - int(seed.shape[1]/2)
    j = y_pos - int(seed.shape[0]/2)

    # Place seed (top left corner at x, y)
    for y in range(seed.shape[0]):
        for x in range(seed.shape[1]):
            universe[(j + y) % ny, (i + x) % nx] = seed[y, x]

    return universe   


def seeded_universe(universe_size, start_seed, start_seed_pos):
    """
        Generate a universe of a given size and populate with a starter seed.

        Parameters
        ----------
        universe_size: tuple
            Tuple of integers representing the width and height of the universe.
        start_seed: str
            Human friendly name for a seed array.
        start_seed_pos: str
            Tuple of integers representing the start seed position.
    """    

    # Initialize an empty universe
    universe = np.zeros((universe_size[1],universe_size[0]))

    # Set desired seed (fallback: infinite)
    seed = SEEDS["infinite"]
    if start_seed in SEEDS.keys():
        seed = SEEDS[start_seed]

    # Determine approx midpoint of the universe (x, y)
    if start_seed_pos[0] < 0 or start_seed_pos[1] < 0:
        pos = (int(universe.shape[1]/2), int(universe.shape[0]/2))
    else:
        pos = start_seed_pos

    # Seed the universe
    universe = place_seed(universe, seed, pos)

    return universe


def create_life(
    universe_size,
    start_seed,
    start_seed_pos,
    quality,
    interval,
    n_generations,
    mayhem,
    mayhem_interval,
    cmap,
    save,
    filename,
):
    """
        Create a Game of Life animation.

        Parameters
        ----------
        universe_size: tuple
            Tuple of integers representing the width and height of the universe.
        start_seed: str
            Human friendly name for a seed array.
        start_seed_pos: str
            Tuple of integers representing the start seed position.
        quality: int
            Resolution of the animation.
        interval: int
            Delay between frames in milliseconds.
        n_generations: int
            Duration (number of frames) of the animation.
        mayhem: bool
            True/false flag for adding randomized chaos to the animation.
        mayhem_interval: int
            Duration between additions of chaos.
        cmap: str
            Color scheme name (see Matplotlib documentation).
        save: bool
            True/false flag to toggle saving of the animation.
        filename: str
            Desired filename for output gif.
    """    

    universe = seeded_universe(universe_size, start_seed, start_seed_pos)

    fig = plt.figure(dpi=quality, figsize=plt.figaspect(universe))
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    plt.axis("off")
    ims = []

    for i in range(n_generations):
        universe = generation(universe)

        if mayhem:
            if i % mayhem_interval == 0:
                xpos = np.random.randint(low=0, high=universe.shape[1])
                ypos = np.random.randint(low=0, high=universe.shape[0])
                universe = place_seed(universe, SEEDS["glider"], (xpos, ypos))
        ims.append((plt.imshow(universe, cmap=cmap),))

    universe_animation = animation.ArtistAnimation(fig, ims, blit=True, interval=interval, repeat=False)

    if save:
        universe_animation.save((str(filename) + ".gif"), writer="imagemagick")
    plt.close()
    
    return universe_animation


if __name__ == "__main__":
    
    # Set up parser to collect command line arguments or display help context
    parser = argparse.ArgumentParser(description="Conway's Game of Life 2.0")

    parser.add_argument("--cmap",
        type=str,
        default="inferno",
        help="Color scheme, in double quotes: \"Greens\". Defaults to inferno.")

    parser.add_argument("--filename",
        type=str,
        default="life",
        help="Desired filename, if --save = True. Defaults to life.")

    parser.add_argument("--interval",
        type=int,
        default=100,
        help="Delay between frames. Defaults to 100.")

    parser.add_argument("--mayhem",
        type=bool,
        default=False,
        help="Add a little mayhem: True or False. Defaults to False.")    

    parser.add_argument("--mayhem-interval",
        type=int,
        default=10,
        help="How often to add mayhem. Defaults to 10.")

    parser.add_argument("--n-generations",
        type=int,
        default=50,
        help="Number of generations. Defaults to 50.")

    parser.add_argument("--quality",
        type=int,
        default=100,
        help="Image quality. Defaults to 100.")

    parser.add_argument("--save",
        type=bool,
        default=True,
        help="Save animation: True or False. Defaults to True.")

    parser.add_argument("--start-seed",
        type=str,
        default="infinite",
        help="Starting seed, in double quotes. Try \"glider\" or \"solid_square\"; check out the README for full list of options. Defaults to infinite")
    
    parser.add_argument("--start-seed-pos",
        type=str,
        default="-1,-1",
        help="Starting seed x,y position, in double quotes. Defaults to the center of the universe.")

    parser.add_argument("--universe-size",
        type=str,
        default="100,100",
        help="Size of the universe, in double quotes: \"width,height\". Defaults to 100 x 100.")

    args = parser.parse_args()

    # Pass command line arguments into life creation function
    create_life(
        universe_size=(
            int(args.universe_size.split(',')[0]),
            int(args.universe_size.split(',')[1])
        ),
        start_seed=args.start_seed,
        start_seed_pos=(
            int(args.start_seed_pos.split(',')[0]),
            int(args.start_seed_pos.split(',')[1])
        ),
        quality=args.quality,
        interval=args.interval,
        n_generations=args.n_generations,
        mayhem=args.mayhem,
        mayhem_interval=args.mayhem_interval,
        cmap=args.cmap,
        save=args.save,
        filename=args.filename
    )