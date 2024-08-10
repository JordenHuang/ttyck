'''
TODO:
'''

import sys,os
import curses, time

DIGITS = [
    [ "0111111","0000011", "0111111", "0111111", "0110011", "0111111", "0111111", "0111111", "0111111", "0111111" ], 
    [ "0110011","0000011", "0000011", "0000011", "0110011", "0110000", "0110000", "0000011", "0110011", "0110011" ], 
    [ "0110011","0000011", "0111111", "0111111", "0111111", "0111111", "0111111", "0000011", "0111111", "0111111" ], 
    [ "0110011","0000011", "0110000", "0000011", "0000011", "0000011", "0110011", "0000011", "0110011", "0000011" ], 
    [ "0111111","0000011", "0111111", "0111111", "0000011", "0111111", "0111111", "0000011", "0111111", "0000011" ], 
]

COLUMN = [
    [ "0000000" ],
    [ "0001100" ],
    [ "0000000" ],
    [ "0001100" ],
    [ "0000000" ],
]

def digit():
    buffer = list()
    cur_time = time.strftime("%H:%M:%S", time.localtime())
    for i in range(len(DIGITS)):
        for x in cur_time:
            if x == ':':
                for c in COLUMN[i][0]:
                    if c == '0':
                        buffer.append(' ')
                    else:
                        buffer.append("\033[42m \033[00m")
            else:
                num = int(x)
                for c in DIGITS[i][num]:
                    if c == '0':
                        buffer.append(' ')
                    else:
                        buffer.append("\033[42m \033[00m")
        buffer.append('\n')
    return buffer

def main(stdscr):
    k = 0
    stdscr.nodelay(True)
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, -1, curses.COLOR_GREEN)
    # stdscr.addstr(5, 5, "Hello, World!", curses.color_pair(1))
    # stdscr.addstr(6, 5, f"{win_width}, {win_height}", curses.color_pair(1))

    while k != ord('q'):
        if k != -1: stdscr.clear()
        win_height, win_width = stdscr.getmaxyx()

        i = win_height//2 - 3
        j = win_width//2 - 7*4
        buffer = digit()
        for c in buffer:
            if c == ' ':
                stdscr.addstr(i, j, ' ', curses.color_pair(1))
                j += 1
            elif c == '\n':
                i += 1
                j = win_width//2 - 7*4
            else:
                stdscr.addstr(i, j, ' ', curses.color_pair(2))
                j += 1
        k = stdscr.getch()
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
    # w = curses.initscr()
    # draw_menu(w)
    # curses.endwin()
