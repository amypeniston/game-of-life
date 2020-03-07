# Game of Life 2.0

![Game of Life 2.0 Icon](https://raw.githubusercontent.com/amypeniston/game-of-life/master/assets/icon.gif)

Game of Life 2.0 is a python-based implementation of Conway's Game of Life -- with a novel ruleset! To generate an animation, run:


```python

python3 life.py

```

Please keep reading for more information on the optional commands that you can use to customize your Game of Life.


*Under Active Development - March 2020*
  

## Setup
  

To get started, navigate to the directory in which you would like to copy the project files.

  
**Option 1:** Clone the repository:

```python

git clone https://github.com/amypeniston/game-of-life.git

```

**Option 2:** Download the repository and extract files into your desired project directory (click the green `Clone or download` button above).


Now there are just a few pesky dependencies to download (if you don't already have them):


```python

pip3 install matplotlib numpy

```

  
## Creating a Universe


After downloading the required dependencies (see above), run the following command to generate a pre-seeded universe and save the output as a `.gif file` within the project directory:


```python

python3 life.py

```


To view the created animation, check the project directory for `life.gif` and open the file your gif viewer or browser.


## Advanced Features


There are an assortment of additional command line arguments that enable you to generate different universes. For example, you can change the [color scheme](https://matplotlib.org/3.1.0/gallery/color/colormap_reference.html?highlight=colormap) by running:

  
```

python3 life.py --cmap "Greens"

```


Likewise, you could change the color scheme **and** add a little mayhem by running:


```python

python3 life.py --cmap "Greens"  --mayhem True

```


For a list of all possible arguments, check the help docs:


```python

python3 life.py --help

```

## Examples

*Coming soon!*
  

## Saving Animations


By default, animations save automatically once generated (with filename: `life.gif`) . If you want to change the filename, use:


```python

python3 life.py --filename "my_universe"

```

## Help

Not sure how this works? Check out:

```python

python3 life.py --help

```

### Troubleshooting: MovieWriter Errors


Different versions of `matplotlib` handle animation creation differently. If you're getting an *MovieWriter imagemagick unavailable* error when you run `python3 life.py`, chances are that the required animation writer library is not installed on your machine.


To fix this, visit the [Imagemagick download page](https://imagemagick.org/script/download.php) and scroll until you see the section that corresponds to the type of machine that you're using. For example, if you're on Windows, find the header "Windows Binary Release".


Download the appropriate Imagemagick version and follow instructions to install on your machine. Be sure to check the box to add the the application directory to your system path. Note: you can optionally check the box to install FFmpeg in addition to Imagemagick; this is a secondary writer than can be used to generate `.gif`s.


Once you have downloaded Imagmagick, you can confirm the animation writers that are available to `matplotlib`:


```python

import matplotlib.animation as animation

animation.writers.list()

>>> ['ffmpeg', 'ffmpeg_file', 'imagemagick', 'imagemagick_file', 'html'] # For example

```
