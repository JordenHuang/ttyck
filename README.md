# ttyck

ttyck (pronounce `tick`) is a cross-platform terminal clock, countdown timer, and a stopwatch.

## Pre-requirements

- Python version >= 3.6
- A terminal that supports ANSI escape code

## Installation

Clone this repository to your computer:

``` shell
git clone https://github.com/JordenHuang/ttyck.git
```

## Usage

Open the terminal, cd to the folder, and run:

```python3
python src/ttyck.py
```

See [Options](#Options) for more option infomations

## Options

``` shell
usage: ttyck [-h] [-cl | -co HOUR MINUTE SECOND | -s] [-u UPDATE_INTERVAL]

A terminal timer tool

options:
  -h, --help            show this help message and exit
  -cl, --clock          clock mode, (default mode)
  -co HOUR MINUTE SECOND, --countdown HOUR MINUTE SECOND
                        countdown timer mode
  -s, --stopwatch       stopwatch mode
  -u UPDATE_INTERVAL, --update-interval UPDATE_INTERVAL
                        set update interval (in seconds), default 0.5 seconds
```
