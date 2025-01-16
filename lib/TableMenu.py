import curses
import logging
import time

from lib.Logger import logger

class TableMenu:
    def __init__(self, config, win):
        self.config = config
        self.is_first_display = True  # флаг для первого отображения
        self.menu_x = 1
        self.menu_y = 1
        self.info_x = 35
        self.info_y = 1
        self.alignment = None
        self.win = win

    def calculate_position(self, width, height, x=None, y=None, Xdo="=", Ydo="="):
        if self.alignment == 'c':
            self.menu_x = (curses.COLS - width) // 2
            self.menu_y = (curses.LINES - height) // 2
            self.info_x = self.menu_x + 35
            self.info_y = self.menu_y
        elif self.alignment == 'r':
            self.menu_x = curses.COLS - width - 1
            self.menu_y = (curses.LINES - height) // 2
            self.info_x = self.menu_x + 35
            self.info_y = self.menu_y
        elif self.alignment == 'l':
            self.menu_x = 1
            self.menu_y = 1
            self.info_x = self.menu_x + 35
            self.info_y = self.menu_y

        if x != None :
            if Xdo == "=":
                self.menu_x = x
                self.info_x = self.menu_x + 35
            elif Xdo == "-":
                self.menu_x = self.menu_x - x
                self.info_x = self.menu_x + 35
            elif Xdo == "+":
                self.menu_x = self.menu_x + x
                self.info_x = self.menu_x + 35
        if y != None:
            if Ydo == "=":
                self.menu_y = y
                self.info_y = self.menu_y
            elif Ydo == "-":
                self.menu_y = self.menu_y - y
                self.info_y = self.menu_y
            elif Ydo == "+":
                self.menu_y = self.menu_y + y
                self.info_y = self.menu_y

    def create_table(self, win, title, options, selected_index, table_width=22):
        def separator_up_info():
            win.addstr("Xx" + "_" * (table_width + 2) + "xX\n")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                #da.play_sound_print()
                win.refresh()

        def separator_centr_info():
            win.addstr("||" + "-" * (table_width + 2) + "||\n")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                #da.play_sound_print()
                win.refresh()

        def separator_down_info():
            win.addstr("Xx" + "¯" * (table_width + 2) + "xX\n")

        separator_up_info()
        #da.play_sound_print()
        win.addstr("|| {:^{width}} ||\n".format(title, width=table_width))
        separator_centr_info()
        #da.play_sound_print()

        for index, option in enumerate(options):
            if index == selected_index:
                option_str = "> {:<{width}}".format(option, width=table_width - 2)
                win.addstr("|| ", curses.color_pair(1))
                win.addstr(option_str, curses.color_pair(2))
                win.addstr(" ||\n", curses.color_pair(1))
            else:
                option_str = "  {:<{width}}".format(option, width=table_width - 2)
                win.addstr("|| ", curses.color_pair(1))
                win.addstr(option_str, curses.color_pair(1))
                win.addstr(" ||\n", curses.color_pair(1))

            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                #da.play_sound_print()
                win.refresh()

        separator_down_info()
        #da.play_sound_print()


    def menu(self, title, options, additional_info=["","","","","",""], alignment="c", x=None, y=None, color='cyan', tips=True, clear=True, info_width=50, Xdo="=", Ydo="="):
        self.alignment = alignment
        curses.curs_set(0)

        icol = {
            1: 'red',
            2: 'green',
            3: 'yellow',
            4: 'blue',
            5: 'magenta',
            6: 'cyan',
            7: 'white'
        }
        col = {v: k for k, v in icol.items()}
        bc = curses.COLOR_BLACK

        curses.start_color()
        curses.init_pair(1, 7, bc)  # normal
        curses.init_pair(2, col[color], bc)  # highlighted

        if clear:
            self.win.clear()
            self.win.refresh()

        self.calculate_position(30, len(options) + 5, x, y, Xdo, Ydo)

        menu_win = curses.newwin(len(options) + 5, 30, self.menu_y, self.menu_x)
        if tips:
            info_win = curses.newwin(len(options) + 5, info_width, self.info_y, self.info_x)

        c = 0
        option = 0
        while c != 10:  # Loop until 'Enter' key (ASCII 10) is pressed
            menu_win.erase()
            if tips:
                info_win.erase()
                info_win.box()
                self.display_info(info_win, additional_info, option)

            # Draw the menu options
            self.create_table(menu_win, title, options, option)

            # Refresh the window to show changes
            menu_win.refresh()
            if tips:
                info_win.refresh()

            # Get user input
            c = self.win.getch()
            logging.info(f"INFO: Key pressed: {c}", exc_info=False)

            if c == curses.KEY_UP:
                option = (option - 1) % len(options)
            elif c == curses.KEY_DOWN:
                option = (option + 1) % len(options)

            self.is_first_display = False

        self.is_first_display = True
        return str(option)

    def display_info(self, info_win, additional_info, option):
        info_lines = additional_info[option].split('\n')
        for i, line in enumerate(info_lines, start=1):
            info_win.addstr(i, 1, line)

    def create_table_text_box(self, win, width):
        def separator_up_info():
            win.addstr(self.menu_y, self.menu_x, "Xx" + "_" * (width + 2) + "xX\n")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                #da.play_sound_print()
                win.refresh()

        def separator_down_info():
            win.addstr(self.menu_y + 2, self.menu_x , "Xx" + "¯" * (width + 2) + "xX\n")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                #da.play_sound_print()
                win.refresh()

        separator_up_info()
        win.addstr(self.menu_y + 1, self.menu_x, "||" + " " * (width + 2) + "||")
        if self.is_first_display:
                time.sleep(self.config.delayOutput)
                #da.play_sound_print()
                win.refresh()
        separator_down_info()

        return [self.menu_x + 3, self.menu_y + 1]



    def text_box(self, table_alignment = "c", clear=True, x=None, y=None, width=22, max_sumbol=22, type="str", Xdo="=", Ydo="="):
        self.alignment = table_alignment

        if clear:
            self.win.clear()
            self.win.refresh()

        self.calculate_position(width+7, 3, x=x, y=y, Xdo=Xdo, Ydo=Ydo)

        c_pozition = self.create_table_text_box(self.win, width)
        self.win.move(c_pozition[1], c_pozition[0])

        curses.curs_set(1)
        text = ""
        c = 0
        while True:  # Бесконечный цикл
            c = self.win.getch()

            logging.info(f"INFO: Key pressed: {c}", exc_info=False)

            if c == 8:
                if len(text) > 0:
                    text = text[:-1]
                    self.win.move(c_pozition[1], c_pozition[0] + len(text))
                    self.win.addstr(' ')
                    #da.play_sound_print()
            elif c == 10:
                self.win.clear()
                self.win.refresh()
                #da.play_sound_print()
                break
            elif type == "str":
                if c < 256 and len(text) < max_sumbol and c != 8:
                    text += chr(c)
                    #da.play_sound_print()
            elif type == "int":
                if c in {48, 49, 50, 51, 52, 53, 54, 55, 56, 57} and len(text) < max_sumbol and c != 8:
                    text += chr(c)
                    #da.play_sound_print()
            elif type == "float":
                if c in {48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 46} and len(text) < max_sumbol and c != 8:
                    text += chr(c)
                    #da.play_sound_print()

            self.win.move(c_pozition[1], c_pozition[0])
            self.win.addstr(text)
            self.win.refresh()

            self.is_first_display = False
        curses.curs_set(0)
        self.is_first_display = True
        return text
