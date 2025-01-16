import curses
import logging
import time
import random as r

from controller.AudioController import audio_controller

class Consolas:
    def __init__(self, config, player, win):
        self.logger = logging.getLogger('Consolas')
        self.config = config
        self.player = player
        self.win = win
        self.table_x = 1
        self.table_y = 1
        self.alignmentTable = None
        self.logger.debug("Consolas initialized")

    def calculate_position(self, width, height, x=None, y=None, Xdo="=", Ydo="="):
        self.logger.debug(f"Calculating position with width={width}, height={height}, x={x}, y={y}, Xdo={Xdo}, Ydo={Ydo}")
        if self.alignmentTable == 'c':
            self.table_x = (curses.COLS - width) // 2
            self.table_y = (curses.LINES - height) // 2
        elif self.alignmentTable == 'r':
            self.table_x = curses.COLS - width - 1
            self.table_y = (curses.LINES - height) // 2
        elif self.alignmentTable == 'l':
            self.table_x = 1
            self.table_y = 1

        if x is not None:
            if Xdo == "=":
                self.table_x = x
            elif Xdo == "-":
                self.table_x -= x
            elif Xdo == "+":
                self.table_x += x
        if y is not None:
            if Ydo == "=":
                self.table_y = y
            elif Ydo == "-":
                self.table_y -= y
            elif Ydo == "+":
                self.table_y += y
        self.logger.debug(f"Calculated position: table_x={self.table_x}, table_y={self.table_y}")


    def fast_loading(self , speed=0.04):
        self.alignmentTable = "c"
        self.calculate_position(24, 3)
        procent = 0

        self.win.addstr(self.table_y, self.table_x, "Xx____________________xX")
        self.win.addstr(self.table_y + 1, self.table_x, "||                    ||")
        self.win.addstr(self.table_y + 2, self.table_x, "Xx¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯xX")

        while procent < 100:
            bar_length = 20
            filled_length = int(bar_length * procent / 100)
            bar = "=" * filled_length + " " * (bar_length - filled_length)

            progress_display = f"Xx________{procent:03d}%________xX"
            self.win.addstr(self.table_y, self.table_x, progress_display)
            self.win.addstr(self.table_y + 1, self.table_x + 2, bar)
            self.win.refresh()

            procent += r.randint(1, 3)

            procent = min(procent, 100)

            time.sleep(speed)

        progress_display = "Xx________100%________xX"
        bar = "=" * bar_length
        self.win.addstr(self.table_y, self.table_x, progress_display)
        self.win.addstr(self.table_y + 1, self.table_x + 2, bar)
        self.win.refresh()

        time.sleep(0.5)
        self.win.clear()



    def create_table(self, *args, style="info", use_clear=True, separator_positions=None, alignment=None, alignmentTable="c", table_width=22, x=None, y=None, Xdo="=", Ydo="="):
        """
        Creates a formatted table on the console window with specified styles and alignments.

        Parameters:
        args: tuple
            The rows of the table to be displayed.
        style: str, optional
            The style of the table, either "info" or "error". Default is "info".
        use_clear: bool, optional
            Whether to clear the window before displaying the table. Default is True.
        separator_positions: list, optional
            Positions where separators should be added between rows.
        alignment: dict, optional
            Alignment for specific rows, with keys as row indices and values as "left", "center", or "right".
        alignmentTable: str, optional#+
            Overall alignment of the table, either "c" for center, "r" for right, or "l" for left. Default is "c".
        table_width: int, optional
            The width of the table. Default is 22.
        x: int, optional
            The x-coordinate for the table's position.
        y: int, optional#+
            The y-coordinate for the table's position.
        Xdo: str, optional
            Operation for x-coordinate adjustment: "=", "+", or "-". Default is "=".
        Ydo: str, optional
            Operation for y-coordinate adjustment: "=", "+", or "-". Default is "=".

        Returns:
        None
        """
        self.logger.debug(f"Creating table with args={args}, style={style}, use_clear={use_clear}, separator_positions={separator_positions}, alignment={alignment}, alignmentTable={alignmentTable}, table_width={table_width}, x={x}, y={y}, Xdo={Xdo}, Ydo={Ydo}")
        self.alignmentTable = alignmentTable
        self.calculate_position(table_width + 7, len(args) + 2, x, y, Xdo, Ydo)

        def separator_up_info():
            self.win.addstr(self.table_y, self.table_x, "Xx" + "_" * (table_width + 2) + "xX")
            self.table_y += 1

        def separator_centr_info():
            self.win.addstr(self.table_y, self.table_x, "||" + "-" * (table_width + 2) + "||")
            self.table_y += 1

        def separator_down_info():
            self.win.addstr(self.table_y, self.table_x, "Xx" + "¯" * (table_width + 2) + "xX")
            self.table_y += 1

        def separator_up_error():
            self.win.addstr(self.table_y, self.table_x, ">>>" + "═" * (table_width + 2) + "<<<")
            self.table_y += 1

        def separator_centr_error():
            self.win.addstr(self.table_y, self.table_x, "!!!" + "-" * (table_width + 2) + "!!!")
            self.table_y += 1

        def separator_down_error():
            self.win.addstr(self.table_y, self.table_x, ">>>" + "═" * (table_width + 2) + "<<<")
            self.table_y += 1

        if use_clear:
            self.win.clear()

        if style == "info":
            separator_up_info()
        elif style == "error":
            separator_up_error()

        audio_controller.play_random_sound_print()
        self.win.refresh()
        time.sleep(self.config.delayOutput)

        if style == "info":
            for index, row in enumerate(args):
                self.win.refresh()
                time.sleep(self.config.delayOutput)

                if len(row) > table_width:
                    words = row.split()
                    lines = []
                    current_line = ""
                    for word in words:
                        if len(current_line) + len(word) + 1 <= table_width:
                            current_line += word + " "
                        else:
                            lines.append(current_line)
                            current_line = word + " "
                    lines.append(current_line)
                    for line in lines:
                        formatted_line = " ".join(line.strip().split())
                        self.win.addstr(self.table_y, self.table_x, "|| {:<{width}} ||".format(formatted_line, width=table_width))
                        self.table_y += 1
                        audio_controller.play_random_sound_print()
                else:
                    if alignment is not None and index in alignment:
                        if alignment[index] == "center":
                            self.win.addstr(self.table_y, self.table_x, "|| {:^{width}} ||".format(row, width=table_width))
                        elif alignment[index] == "right":
                            self.win.addstr(self.table_y, self.table_x, "|| {:>{width}} ||".format(row, width=table_width))
                    else:
                        self.win.addstr(self.table_y, self.table_x, "|| {:<{width}} ||".format(row, width=table_width))
                    self.table_y += 1
                    audio_controller.play_random_sound_print()

                if separator_positions is not None and index in separator_positions:
                    separator_centr_info()

        elif style == "error":
            for index, row in enumerate(args):
                self.win.refresh()
                time.sleep(self.config.delayOutput)

                if len(row) > table_width:
                    words = row.split()
                    lines = []
                    current_line = ""
                    for word in words:
                        if len(current_line) + len(word) + 1 <= table_width:
                            current_line += word + " "
                        else:
                            lines.append(current_line)
                            current_line = word + " "
                    lines.append(current_line)
                    for line in lines:
                        formatted_line = " ".join(line.strip().split())
                        self.win.addstr(self.table_y, self.table_x, "!!! {:<{width}} !!!".format(formatted_line, width=table_width))
                        self.table_y += 1
                        audio_controller.play_random_sound_print()
                else:
                    if alignment is not None and index in alignment:
                        if alignment[index] == "center":
                            self.win.addstr(self.table_y, self.table_x, "!!! {:^{width}} !!!".format(row, width=table_width))
                        elif alignment[index] == "right":
                            self.win.addstr(self.table_y, self.table_x, "!!! {:>{width}} !!!".format(row, width=table_width))
                    else:
                        self.win.addstr(self.table_y, self.table_x, "!!! {:<{width}} !!!".format(row, width=table_width))
                    self.table_y += 1
                    audio_controller.play_random_sound_print()

                if separator_positions is not None and index in separator_positions:
                    separator_centr_error()

        self.win.refresh()
        time.sleep(self.config.delayOutput)
        if style == "info":
            separator_down_info()
        elif style == "error":
            separator_down_error()

        audio_controller.play_random_sound_print()
        self.win.refresh()
        self.logger.debug("Table created")


    def play_animation(self, frames, delay=0.3, alignmentTable="c", x=None, y=None, clear=True, Xdo="=", Ydo="=", audio=True):
        self.logger.debug(f"Playing animation with frames={frames}, delay={delay}, alignmentTable={alignmentTable}, x={x}, y={y}, clear={clear}, Xdo={Xdo}, Ydo={Ydo}, audio={audio}")
        self.alignmentTable = alignmentTable
        self.calculate_position(len(frames[0]), len(frames), x, y, Xdo, Ydo)

        if clear:
            self.win.clear()

        for frame in frames:
            self.win.addstr(self.table_y, self.table_x, frame)
            if audio:
                audio_controller.play_random_sound_print()
            self.win.refresh()
            curses.napms(int(delay * 1000))
            self.table_y += 1

        self.win.refresh()
        self.logger.debug("Animation played")


    def display_map(self, map_array, player, alignmentTable="c", x=None, y=None, Xdo="=", Ydo="="):
        self.logger.debug(f"Displaying map with player position x={player.x}, y={player.y}")
        self.alignmentTable = alignmentTable

        self.win.clear()
        self.win.refresh()

        self.calculate_position(len(map_array[0]), len(map_array), x, y, Xdo, Ydo)

        for row_index, row in enumerate(map_array):
            for char_index, char in enumerate(row):
                table_x = self.table_x + char_index
                table_y = self.table_y + row_index

                if player.x == char_index and player.y == row_index:
                    self.win.addch(table_y, table_x, '@', curses.color_pair(2))
                elif not self.player.playerMap and (abs(player.x - char_index) > 3 or abs(player.y - row_index) > 3):
                    self.win.addch(table_y, table_x, ' ')
                else:
                    self.win.addch(table_y, table_x, char)
            self.win.refresh()
            audio_controller.play_random_sound_print()
            time.sleep(0.02)

        self.win.refresh()
        self.logger.debug("Map displayed")


    def loading_animation(self, imports):
        self.logger.debug(f"Starting loading animation for imports={imports}")
        animation_symbols = ['|', '/', '-', '\\']
        max_length = max(len(module) for module in imports)
        height, width = self.win.getmaxyx()
        y = 0
        for module in imports:
            module_text = f"| {module}{' '*(max_length - len(module))} "
            if len(module_text) + max_length + 6 > width - 1:
                module_text = module_text[:width - max_length - 7]
            self.win.addstr(y, 0, module_text)
            for i in range(r.randint(2, 6)):
                if max_length + 4 < width - 1:
                    self.win.addstr(y, max_length + 4, animation_symbols[i % len(animation_symbols)])
                self.win.refresh()
                time.sleep(0.1)
                if max_length + 4 < width - 1:
                    self.win.addstr(y, max_length + 4, ' ')
            if max_length + 4 < width - 1:
                self.win.addstr(y, max_length + 4, "DONE |")
            self.win.refresh()
            time.sleep(r.uniform(0.02, 0.09))
            y += 1
        self.win.refresh()
        self.logger.debug("Loading animation completed")