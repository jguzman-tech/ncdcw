#!/usr/bin/env python3

import bs4
import requests
import sys
import curses
import time
import signal
import datetime
import pickle
import textwrap

def cleanup(signal=None, frame=None):
    curses.endwin()
    sys.exit(0)

def get_def_div(bs):
    count = 1
    result = bs.find('div', {'value': count})
    while result:
        yield result
        count += 1
        result = bs.find('div', {'value': count})

def get_content(word):
    try:
        response = pickle.load(open(f'./cache/{word}.pkl', 'rb'))
    except:
        response = requests.get('https://dictionary.com/browse/' + word)
        try:
            pickle.dump(response, open(f'./cache/{word}.pkl', 'wb'))
        except:
            # will occur if dir does not exist or you don't have write perms
            pass
    if(response.status_code == 200):
        bs = bs4.BeautifulSoup(response.content, 'html.parser')
        g = get_def_div(bs)
        definitions = []
        for div in g:
            if len(div.text) > 0:
                definitions.append(div)
        categories = bs.find_all('span', {'class', 'luna-pos'})
        return definitions, categories
    else:
        return None, None

def prompt_word(stdscr):
    stdscr.clear()
    prompt = "Enter a word (or 'q' to quit): "
    stdscr.addstr(prompt)
    stdscr.refresh()

    word = ""
    c = ""
    while True:
        c = stdscr.getch()
        if c == ord('\n'):
            break
        elif c == curses.KEY_BACKSPACE:
            if len(word) != 0:
                stdscr.move(0, len(prompt) + len(word) - 1)
                stdscr.addch(' ')
                stdscr.move(0, len(prompt) + len(word) - 1)
                stdscr.refresh()
                word = word[0:-1]
        else:
            if chr(c).isprintable():
                word += chr(c)
                stdscr.move(0, len(prompt) + len(word) - 1)
                stdscr.addch(chr(c))
                stdscr.refresh()
    return word

if __name__ == '__main__':
    stdscr = curses.initscr()
    
    signal.signal(signal.SIGINT, cleanup)

    stdscr.keypad(1)
    curses.noecho()

    while True:
        word = prompt_word(stdscr)
        if word == 'q':
            break
        definitions, categories = get_content(word)
        
        lpad = (curses.COLS - len(word)) // 2
        stdscr.clear()
        stdscr.move(0, lpad)
        stdscr.addstr(word.upper())
        stdscr.move(2, 0)

        if definitions is not None and categories is not None:
            count = 0
            cat_ndx = 0
            text = ""
            for definition in definitions:
                if categories[cat_ndx].sourcepos > definition.sourcepos:
                    cat_ndx += 1
                fmt_str = (f"{count}: "
                           f"({categories[cat_ndx].text}) "
                           f"{definition.text}\n")
                text += fmt_str
                count += 1

        tlines = textwrap.wrap(text, curses.COLS-1, replace_whitespace=False)
        content = "\n".join(tlines)
        pad_lines = content.count('\n')
        pad_n = 0
        
        pad = curses.newpad(pad_lines+2, curses.COLS)
        stdscr.refresh()
        pad.addstr(content)
        pad.refresh(0, 0, 1, 0, curses.LINES-2, curses.COLS)

        stdscr.move(curses.LINES-1, 0)
        stdscr.addstr("'q' to quit or <ENTER> to lookup another word", curses.A_REVERSE)
        stdscr.refresh()
        
        c = ""
        while c != ord('q') and c != ord('\n'):
            c = stdscr.getch()
            
            if c == curses.KEY_UP:
                pad_n -= 1
            elif c == curses.KEY_DOWN:
                pad_n += 1

            if pad_n > pad_lines - curses.LINES:
                pad_n = pad_lines - curses.LINES
            elif pad_n < 0:
                pad_n = 0
            
            pad.refresh(pad_n, 0, 1, 0, curses.LINES-2, curses.COLS)
            stdscr.refresh()

        if c == ord('q'):
            cleanup()

    curses.endwin()
