# Image to ASCII converter

Converts image (and also video) to ASCII art, and saves it to any image file (or mp4 / gif file).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli-usage)
  - [Others](#other-usage)
- [Example](#example)
- [WIP](#wip)

&nbsp;

## Installation

Download the repo, or use

```
git clone https://github.com/bryanluwz/img2ascii
```

to download the repo to your current directory.

&nbsp;

Install the modules needed for the python program by running

```
pip install -r requirements.txt
```

&nbsp;

## Usage

### CLI usage

#### For image

```
python img2ascii_cli.py -i path/to/image.ext
```

#### For video

```
python img2ascii_cli.py -v path/to/video.ext [-cs COMPRESSION_SPEED]
```

Compression speed ranges from 0 - 9, with 0 being the slowest, and 9 the fastest. Slower compression speed means longer waiting time, but higher compression rate (though the output video still has quite a file size).


Output file will be in the same directory as the input file, with "_ascii" appended to the end of the file name.

&nbsp;

### Other usage

For direct execution of the Python file, just change the file path in the main function.

&nbsp;

## Example

![rick rolled lol](./examples/rick_roll_ascii.gif)

&nbsp;

## Some things I might add / fix ~~<sub><sub>I probably won't</sub></sub>~~

- Better remaining time estimation
- More user options in CLI
- Coloured ASCII?
- Better README file
