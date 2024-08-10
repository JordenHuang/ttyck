# TODO:
# 1. add getch()
# 2. add countdown timer
# 3. add check argc and argv utility

import sys, os
import time, datetime
import tick_util as tutil


DIGITS_WIDTH = 7
DIGITS_HEIGHT = 5
DIGITS_HALF_WIDTH = 3
DIGITS_HALF_HEIGHT = 2

DIGITS = [
    "01111110110011011001101100110111111",
    "00000110000011000001100000110000011",
    "01111110000011011111101100000111111",
    "01111110000011011111100000110111111",
    "01100110110011011111100000110000011",
    "01111110110000011111100000110111111",
    "01111110110000011111101100110111111",
    "01111110000011000001100000110000011",
    "01111110110011011111101100110111111",
    "01111110110011011111100000110000011"
]


COLON = [
    "00000000001100000000000011000000000"
]


class Term:
    term_cols, term_rows = os.get_terminal_size()
    center_row = term_rows//2 + 1
    center_col = term_cols//2 + 1
    size_has_changed = False

    text_color = tutil.Colors.bg.green
    text_color_re = tutil.Colors.fg.green

    def updata_win_size(self):
        self.size_has_changed = False
        col, row = os.get_terminal_size()
        if col != self.term_cols or row != self.term_rows:
            self.size_has_changed = True
            self.term_cols = col
            self.term_rows = row
            self.center_row = self.term_rows//2 + 1
            self.center_col = self.term_cols//2 + 1

    def win_too_small(self):
        if self.term_cols < DIGITS_WIDTH * 8 or self.term_rows < DIGITS_HEIGHT:
            return True
        else:
            return False

def change_text_color(win:Term, key:str):
    if key == '0':
        win.text_color    = tutil.Colors.bg.black
        win.text_color_re = tutil.Colors.fg.black
    if key == '1':
        win.text_color    = tutil.Colors.bg.red
        win.text_color_re = tutil.Colors.fg.red
    if key == '2':
        win.text_color    = tutil.Colors.bg.green
        win.text_color_re = tutil.Colors.fg.green
    if key == '3':
        win.text_color    = tutil.Colors.bg.yellow
        win.text_color_re = tutil.Colors.fg.yellow
    if key == '4':
        win.text_color    = tutil.Colors.bg.blue
        win.text_color_re = tutil.Colors.fg.blue
    if key == '5':
        win.text_color    = tutil.Colors.bg.magenta
        win.text_color_re = tutil.Colors.fg.magenta
    if key == '6':
        win.text_color    = tutil.Colors.bg.cyan
        win.text_color_re = tutil.Colors.fg.cyan
    if key == '7':
        win.text_color    = tutil.Colors.bg.white
        win.text_color_re = tutil.Colors.fg.white
    return win



def rander_digit(win:Term, digit:str, pos:int):
    '''
        position: from 0 to 7, i.e. 00:01:30
                                    0  ->  7
    '''
    # The starting row and col to put text
    srow = win.center_row - DIGITS_HEIGHT//2
    scol = win.center_col + DIGITS_WIDTH*(-4 + pos)
    if digit == ':':
        for i in range(DIGITS_HEIGHT):
            for j in range(DIGITS_WIDTH):
                if COLON[0][i*DIGITS_WIDTH + j] == '1':
                    tutil.put_text(srow+i, scol+j, ' ', win.text_color)
                else:
                    tutil.put_text(srow+i, scol+j, ' ')
    else:
        for i in range(DIGITS_HEIGHT):
            for ch in range(len(digit)):
                cells = DIGITS[int(digit[ch])]
                for j in range(DIGITS_WIDTH):
                    if cells[i*DIGITS_WIDTH + j] == '1':
                        tutil.put_text(srow+i, scol+ch*DIGITS_WIDTH+j, ' ', win.text_color)
                    else:
                        tutil.put_text(srow+i, scol+ch*DIGITS_WIDTH+j, ' ')
    # Move to the text place to prevent key press's echo
    tutil.move_to(srow, scol)



def clock(win:Term, fps:int):
    while True:
        sys.stdout.flush()
        time.sleep(1/fps)

        # Process key press
        keypress = tutil.getch()
        if keypress != -1:
            if keypress == 'q' or keypress == '\033':
                break
            elif 47 < ord(keypress) and ord(keypress) < 58 :
                win = change_text_color(win, keypress)

        # Update (check) window size
        win.updata_win_size()
        if win.size_has_changed:
            tutil.clear_screen()

        # Main rander part
        cur_time = time.strftime("%H:%M:%S", time.localtime())
        if win.win_too_small():
            # if terminal width less than 8 character width or less than 1 character height
            tutil.put_text(win.center_row, win.center_col - 4, cur_time, win.text_color_re)
        else:
            i = 0
            for digit in cur_time:
                rander_digit(win, digit, i)
                i += 1

def stopwatch(win:Term, fps:int):
    hour = 0
    min  = 0
    sec  = 0

    last_hour = -1
    last_min = -1
    last_sec = -1

    timer_stop = False
    last_time = time.time()
    while True:
        sys.stdout.flush()
        time.sleep(1/fps)

        # Process key press
        keypress = tutil.getch()
        if keypress != -1:
            if keypress == 'q' or keypress == '\033':
                break
            elif keypress == ' ':
                if timer_stop == False: timer_stop = True
                else: timer_stop = False
            elif 47 < ord(keypress) and ord(keypress) < 58 :
                # Clear last_* variables, in order to rerender them
                last_hour = last_min = last_sec = -1
                win = change_text_color(win, keypress)

        # Timer stoped
        if timer_stop == True: continue

        # Update variables
        now = time.time()
        # tutil.put_text(1, 1, f"{now - last_time}")
        laptime = now - last_time
        if laptime >= 1:
            last_time = now
            sec += 1
            if sec == 60:
                min += 1
                sec = sec % 60
            if min == 60:
                hour += 1
                min = min % 60

        # Update (check) window size
        win.updata_win_size()
        if win.size_has_changed:
            tutil.clear_screen()
            last_hour = last_min = last_sec = -1

        # Main rander part
        if win.win_too_small():
            cur_time = "{:02d}:{:02d}:{:02d}".format(hour, min, sec)
            tutil.put_text(win.center_row, win.center_col - 4, cur_time, win.text_color_re)
        else:
            if hour != last_hour:
                last_hour = hour
                rander_digit(win, "{:02d}".format(hour), 0)
            if min != last_min:
                last_min = min
                rander_digit(win, "{:02d}".format(min), 3)
            if sec != last_sec:
                last_sec = sec
                rander_digit(win, "{:02d}".format(sec), 6)
            rander_digit(win, ":", 2)
            rander_digit(win, ":", 5)

def countdown_timer(win:Term, fps:int, time_value:tuple):
    hour = time_value[0]
    min  = time_value[1]
    sec  = time_value[2]

    timer_stop = False
    time_up = False
    last_time = time.time()
    while True:
        sys.stdout.flush()
        time.sleep(1/fps)

        # Process key press
        keypress = tutil.getch()
        if keypress != -1:
            if keypress == 'q' or keypress == '\033':
                break
            elif keypress == ' ':
                if timer_stop == False: timer_stop = True
                else: timer_stop = False
            elif keypress == 'r':
                tutil.clear_screen()
                time_up = False
                timer_stop = False
                hour = time_value[0]
                min  = time_value[1]
                sec  = time_value[2]
            elif 47 < ord(keypress) and ord(keypress) < 58 :
                # Clear last_* variables, in order to rerender them
                last_hour = last_min = last_sec = -1
                win = change_text_color(win, keypress)

        # Timer stoped
        if timer_stop == True: continue

        # Update variables
        if sec != 0 or min != 0 or hour != 0:
            now = time.time()
            laptime = now - last_time
            if laptime >= 1:
                last_time = now
                sec -= 1
                if sec < 0:
                    min -= 1
                    sec += 60
                    if min < 0 and hour > 0:
                        min += 60
                        hour -= 1
        else:
            time_up = True

        # Update (check) window size
        win.updata_win_size()
        if win.size_has_changed:
            tutil.clear_screen()
            last_hour = last_min = last_sec = -1

        # Main rander part
        if not time_up and win.win_too_small():
            cur_time = "{:02d}:{:02d}:{:02d}".format(hour, min, sec)
            tutil.put_text(win.center_row, win.center_col - 4, cur_time, win.text_color_re)
        elif not time_up:
            rander_digit(win, "{:02d}".format(hour), 0)
            rander_digit(win, ":", 2)
            rander_digit(win, "{:02d}".format(min), 3)
            rander_digit(win, ":", 5)
            rander_digit(win, "{:02d}".format(sec), 6)
        else:
            # Show message when time's up
            tutil.put_text(win.center_row-1, win.center_col - 5, "           ", tutil.Colors.fg.red)
            tutil.put_text(win.center_row,   win.center_col - 5, " Time's up ", tutil.Colors.fg.red)
            tutil.put_text(win.center_row+1, win.center_col - 5, "           ", tutil.Colors.fg.red)


def main():
    win = Term()
    time_value = (0, 0, 10)

    tutil.start_alt_buffer()
    tutil.clear_screen()
    tutil.cursor_invisible()

    # clock(win, 30)
    # stopwatch(win, 60)
    countdown_timer(win, 60, time_value)

    tutil.cursor_visible()
    tutil.clear_screen()
    tutil.end_alt_buffer()



main()

