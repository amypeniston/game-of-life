import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse

def generation(universe):
    new_universe = np.copy(universe)

    for i in range(universe.shape[0]):
        for j in range(universe.shape[1]):
            new_universe[i, j] = apply_rules(i, j, universe)
    return new_universe


def apply_rules(i, j, universe):
    # Toroidal boundary conditions (cells wrap around the screen)
    ny = universe.shape[0]
    nx = universe.shape[1]

    num_neighbors = int((universe[i, (j-1)%nx] + universe[i, (j+1)%nx] + 
                         universe[(i-1)%ny, j] + universe[(i+1)%ny, j] + 
                         universe[(i-1)%ny, (j-1)%nx] + universe[(i-1)%ny, (j+1)%nx] + 
                         universe[(i+1)%ny, (j-1)%nx] + universe[(i+1)%ny, (j+1)%nx]))

    # Apply rules
    if universe[i, j] and not 2 <= num_neighbors <= 3:
        return 0
    elif num_neighbors == 3:
        return 1
    return universe[i, j]

def random_universe(universe_size):

    # Initialize an empty universe
    universe = np.zeros(universe_size)

    # Set up an infinite seed
    seed_array = np.array([
        [1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1],
    ])

    seed_array = np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ])

    ny = universe.shape[0]
    nx = universe.shape[1]

    # Determine midpoint of the universe
    x_mid, y_mid = int(nx/2), int(ny/2)

    # Determine top left corner position
    i = x_mid - int(seed_array.shape[0]/2)
    j = y_mid - int(seed_array.shape[1]/2)

    #x_seed_end, y_seed_end = x_seed_start + seed_array.shape[1], y_seed_start + seed_array.shape[0]
    #universe[y_seed_start:y_seed_end, x_seed_start:x_seed_end] = seed_array

    for y in range(seed_array.shape[0]):
        for x in range(seed_array.shape[1]):
            universe[(i+y)%ny, (j+x)%nx] = seed_array[y, x]

    return universe



def add_glider(pos, universe):
    j, i = pos # x,y

    ny = universe.shape[0]
    nx = universe.shape[1]
    
    glider = np.array([[0, 0, 1],
                       [1, 0, 1],
                       [0, 1, 1]])
    
    for y in range(glider.shape[0]):
        for x in range(glider.shape[1]):
            universe[(i+y)%ny, (j+x)%nx] = glider[y, x]

    return universe


def start_life(
    universe_size,
    quality,
    figsize,
    interval,
    n_generations,
    mayhem,
    mayhem_interval,
    cmap,
    save,
    filename,
):

    universe = random_universe(universe_size)

    fig = plt.figure(figsize=figsize, dpi=quality)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    plt.axis("off")
    ims = []

    for i in range(n_generations):
        universe = generation(universe)

        if mayhem:
            if i % mayhem_interval == 0:
                xpos = np.random.randint(low=0, high=universe.shape[0])
                ypos = np.random.randint(low=0, high=universe.shape[1])
                universe = add_glider((xpos,ypos), universe)
        ims.append((plt.imshow(universe, cmap=cmap),))

    universe_animation = animation.ArtistAnimation(fig, ims, blit=True, interval=interval, repeat=False)

    if save:
        universe_animation.save((str(filename) + ".gif"), writer="imagemagick")
    plt.close()
    
    return universe_animation


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conway's Game of Life 2.0")

    parser.add_argument("--universe-size",
        type=str,
        default="100,100",
        help="Size of the universe, in quotes (x, y). Defaults to 100,100.")

    parser.add_argument("--quality",
        type=int,
        default=100,
        help="Image quality. Defaults to 100.")
    
    parser.add_argument("--interval",
        type=int,
        default=100,
        help="Delay between frames. Defaults to 100.")

    parser.add_argument("--n-generations",
        type=int,
        default=50,
        help="Number of generations. Defaults to 50.")

    parser.add_argument("--mayhem",
        type=bool,
        default=False,
        help="Add a little mayhem. Defaults to False.")    

    parser.add_argument("--mayhem-interval",
        type=int,
        default=10,
        help="How often to add mayhem. Defaults to 10.")

    parser.add_argument("--cmap",
        type=str,
        default="inferno",
        help="Color scheme, in quotes. Defaults to inferno.")

    parser.add_argument("--save",
        type=bool,
        default=True,
        help="Save animation? Defaults to True.")

    parser.add_argument("--filename",
        type=str,
        default="life",
        help="Desired filename, if --save = True. Defaults to life.")

    args = parser.parse_args()



    start_life(
        universe_size=(
            int(args.universe_size.split(',')[1]),
            int(args.universe_size.split(',')[0])
        ),
        quality=args.quality,
        figsize=(8,8),
        interval=args.interval,
        n_generations=args.n_generations,
        mayhem=args.mayhem,
        mayhem_interval=args.mayhem_interval,
        cmap=args.cmap,
        save=args.save,
        filename=args.filename
    )