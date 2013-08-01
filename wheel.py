from collections import deque
import curses
from functools import partial
from itertools import chain, islice, repeat, tee
from random import randrange, shuffle
from time import sleep


def display(screen, state, width=3):
    for k, v in enumerate(state):
        screen.addstr(k, 3, str(v).center(width + 2))

    screen.addstr(5, width + 5, '\u2190')
    screen.addstr(11, 0, '')


def pause(n):
    def f():
        return sleep(n)
    return f


def pauses():
    yield from chain(
        repeat(pause(0), 2500),
        repeat(pause(.001), 1250),
        repeat(pause(.005), 500),
        repeat(pause(.01), 250),
        repeat(pause(.05), 100),
        repeat(pause(.1), 50),
        repeat(pause(.5), 25),
        repeat(pause(1), randrange(5, 8)),
    )


def spin(screen, wheel):
    display(screen, islice(wheel, 11))
    screen.refresh()
    curses.beep()
    wheel.rotate(1)


def wheel(n):
    values = deque(range(1, n + 1))
    shuffle(values)
    return values


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()

    text1 = partial(stdscr.addstr, 4, 12)
    text2 = partial(stdscr.addstr, 5, 12)

    text1('   Welcome to the')
    text2('Showcase Showdown')

    colors = (
        (1, curses.COLOR_RED, curses.COLOR_BLACK),
        (2, curses.COLOR_GREEN, curses.COLOR_BLACK),
    )

    for color in colors:
        curses.init_pair(*color)

    red = lambda: curses.color_pair(1)
    green = lambda: curses.color_pair(2)

    wheel = wheel(15)

    try:
        for pause in pauses():
            spin(stdscr, wheel)
            pause()

        text1(' ' * 17)
        text2(' ' * 17)

        stdscr.addstr(5, 8, '\u2190', green())

        winner = partial(stdscr.addstr, 5, 11)

        for x in range(11):
            if x % 2:
                winner(' ' * 11)
            else:
                winner('WINNER!!!!!', red() | curses.A_BOLD)

            stdscr.addstr(11, 0, '')
            stdscr.refresh()
            sleep(1)

        stdscr.addstr(12, 0, 'Press any key to exit...')
        stdscr.getch()
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
