import curses

def main(stdscr):
    stdscr.keypad(True)
    curses.noecho()
    while True:
        c = stdscr.getch()
        stdscr.addstr(0, 0, f"KEY: {c}   ")
        stdscr.refresh()
        if c == 27:  # ESC для выхода
            break

curses.wrapper(main)