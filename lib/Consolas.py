import curses
import threading
import time
import random as r

import keyboard

from controller.AudioController import audio_controller

from lib.Logger import logger

class Consolas:
    def __init__(self, config, player, win):
        self.config = config
        self.player = player
        self.win = win
        self.tab_active = False
        self.current_focus = 0
        logger.info("Consolas initialized")

    def clear_window(self):
        self.win.clear()
        self.win.refresh()

    def calculate_position(self, width, height, alignmentTable, x=None, y=None, Xdo="=", Ydo="="):
        max_y, max_x = self.win.getmaxyx()
        absolute_center_x = (max_x - width) // 2
        absolute_center_y = (max_y - height) // 2

        if alignmentTable == 'c':
            self.table_x, self.table_y = absolute_center_x, absolute_center_y
        elif alignmentTable == 'r':
            self.table_x = max_x - width - 1
            self.table_y = absolute_center_y
        elif alignmentTable == 'l':
            self.table_x, self.table_y = 1, 1

        if x is not None:
            self.table_x = x if Xdo == "=" else self.table_x + x * (1 if Xdo == "+" else -1)
        if y is not None:
            self.table_y = y if Ydo == "=" else self.table_y + y * (1 if Ydo == "+" else -1)

        return self.table_x, self.table_y

    #——————————————————————————————create widgets——————————————————————————————

    def fast_loading(self, speed=0.04):
        return self.Fastloading(self, speed)

    def create_table(self, *args, **kwargs):
        return self.Table(self, *args, **kwargs)

    def play_animation(self, frames, delay=0.3, alignmentTable="c", x=None, y=None, clear=True, Xdo="=", Ydo="=", audio=True):
        return self.Animation(self, frames, delay, alignmentTable, x, y, clear, Xdo, Ydo, audio)

    def loading_animation(self):
        return self.loadingAnimation(self)

    def create_menu(self, title, options, additional_info=None, alignment="c", x=None, y=None, color='cyan', tips=True, clear=True, info_width=50, table_width=22, Xdo="=", Ydo="="):
        return self.Menu(self, title, options, additional_info, alignment, x, y, color, tips, clear, info_width, table_width, Xdo, Ydo)

    def create_text_box(self, table_alignment="c", clear=True, x=None, y=None, width=22, max_sumbol=22, input_type="str", Xdo="=", Ydo="="):
        return self.TextBox(self, table_alignment, clear, x, y, width, max_sumbol, input_type, Xdo, Ydo)

    #——————————————————————————————tab control——————————————————————————————

    def start_tab_control(self, widgets: list):
        self.tab_active = True
        current_focus = 0
        widgets[current_focus].toggle_pause()

        self.win.keypad(True)
        curses.mousemask(1)

        while self.tab_active:
            c = self.win.getch()

            if c == 9 or c == curses.KEY_BTAB:
                widgets[current_focus].toggle_pause()

                if c == 9:
                    current_focus = (current_focus + 1) % len(widgets)
                    audio_controller.play_random_sound_print()
                else:
                    current_focus = (current_focus - 1) % len(widgets)
                    audio_controller.play_random_sound_print()

                widgets[current_focus].toggle_pause()

            elif c == 27:
                self.stop_tab_control()

    def stop_tab_control(self):
        self.tab_active = False
        self.win.keypad(False)
        curses.mousemask(0)

    #——————————————————————————————widgets——————————————————————————————

    class Fastloading():
        def __init__(self, parent, speed=0.04):
            self.parent = parent
            self.win = parent.win
            self.speed = speed

            self.run()

        def run(self):
            table_x,table_y = self.parent.calculate_position(24, 3, "c")
            procent = 0

            self.win.addstr(table_y, table_x, "Xx____________________xX")
            self.win.addstr(table_y + 1, table_x, "||                    ||")
            self.win.addstr(table_y + 2, table_x, "Xx¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯xX")

            while procent < 100:
                bar_length = 20
                filled_length = int(bar_length * procent / 100)
                bar = "=" * filled_length + " " * (bar_length - filled_length)

                progress_display = f"Xx________{procent:03d}%________xX"
                self.win.addstr(table_y, table_x, progress_display)
                self.win.addstr(table_y + 1, table_x + 2, bar)
                self.win.refresh()

                procent += r.randint(1, 3)

                procent = min(procent, 100)

                time.sleep(self.speed)

            progress_display = "Xx________100%________xX"
            bar = "=" * bar_length
            self.win.addstr(table_y, table_x, progress_display)
            self.win.addstr(table_y + 1, table_x + 2, bar)
            self.win.refresh()

            time.sleep(0.5)
            self.win.clear()

    class Table:
        def __init__(self, parent, *args, style="info", clear=True, separator_positions=None,
                    alignment=None, alignmentTable="c", table_width=22, x=None, y=None,
                    Xdo="=", Ydo="="):
            self.parent = parent
            self.win = parent.win
            self.config = parent.config
            self.player = parent.player

            self.args = args
            self.style = style
            self.clear = clear
            self.separator_positions = separator_positions
            self.alignment = alignment
            self.alignmentTable = alignmentTable
            self.table_width = table_width
            self.x, self.y = x, y
            self.Xdo, self.Ydo = Xdo, Ydo

            self.table()

        def table(self):

            self.table_x, self.table_y = self.parent.calculate_position(
                self.table_width + 7, len(self.args) + 2, self.alignmentTable,
                self.x, self.y, self.Xdo, self.Ydo
            )

            if self.clear:
                self.win.clear()

            self._draw_table_header()
            self._draw_table_content()
            self._draw_table_footer()

            audio_controller.play_random_sound_print()
            self.win.refresh()
            logger.info("Table created")

        def _draw_table_header(self):
            if self.style == "info":
                self._separator_up_info()
            elif self.style == "error":
                self._separator_up_error()

            audio_controller.play_random_sound_print()
            self.win.refresh()
            time.sleep(self.config.delayOutput)

        def _draw_table_content(self):
            for index, row in enumerate(self.args):
                self.win.refresh()
                time.sleep(self.config.delayOutput)

                if len(row) > self.table_width:
                    self._draw_long_row(row)
                else:
                    self._draw_short_row(row, index)

                if self.separator_positions and index in self.separator_positions:
                    self._draw_separator()

        def _draw_table_footer(self):
            self.win.refresh()
            time.sleep(self.config.delayOutput)

            if self.style == "info":
                self._separator_down_info()
            elif self.style == "error":
                self._separator_down_error()

        def _draw_long_row(self, row):
            words = row.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= self.table_width:
                    current_line += word + " "
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            for line in lines:
                formatted_line = " ".join(line.strip().split())
                self._write_line(formatted_line)

        def _draw_short_row(self, row, index):
            if self.alignment and index in self.alignment:

                align = self.alignment[index]
                if align == "c":
                    format_spec = "{:^{width}}"
                elif align == "r":
                    format_spec = "{:>{width}}"
                elif align == "l":
                    format_spec = "{:<{width}}"
                else:
                    logger.warning(f"Invalid alignment '{align}' for row {index}, defaulting to left alignment.")
                    format_spec = "{:<{width}}"
            else:
                format_spec = "{:<{width}}"

            self._write_line(row, format_spec)


        def _write_line(self, text, format_spec="{:<{width}}"):
            border = "||" if self.style == "info" else "!!!"
            try:
                line = f"{border} {format_spec.format(text, width=self.table_width)} {border}"
                self.win.addstr(self.table_y, self.table_x, line)
                self.table_y += 1
                audio_controller.play_random_sound_print()
            except ValueError as e:
                logger.error(f"Error formatting line with text='{text}', format_spec='{format_spec}': {e}")
                raise


        def _draw_separator(self):
            if self.style == "info":
                self._separator_center_info()
            elif self.style == "error":
                self._separator_center_error()


        def _separator_up_info(self):
            self._draw_separator_line("Xx", "_", "xX")

        def _separator_center_info(self):
            self._draw_separator_line("||", "-", "||")

        def _separator_down_info(self):
            self._draw_separator_line("Xx", "¯", "xX")

        def _separator_up_error(self):
            self._draw_separator_line(">>>", "═", "<<<")

        def _separator_center_error(self):
            self._draw_separator_line("!!!", "-", "!!!")

        def _separator_down_error(self):
            self._draw_separator_line(">>>", "═", "<<<")

        def _draw_separator_line(self, left, middle, right):
            line = f"{left}{middle * (self.table_width + 2)}{right}"
            self.win.addstr(self.table_y, self.table_x, line)
            self.table_y += 1

    class Animation():
        def __init__(self, parent, frames, delay=0.3, alignmentTable="c", x=None, y=None, clear=True, Xdo="=", Ydo="=", audio=True):
            self.parent = parent
            self.win = parent.win

            self.frames = frames
            self.delay = delay
            self.alignmentTable = alignmentTable
            self.x = x
            self.y = y
            self.clear = clear
            self.Xdo = Xdo
            self.Ydo = Ydo
            self.audio = audio

            self.play_animation()

        def play_animation(self):
            table_x, table_y =self.parent.calculate_position(len(self.frames[0]), len(self.frames), self.alignmentTable, self.x, self.y, self.Xdo, self.Ydo)

            if self.clear:
                self.win.clear()

            for frame in self.frames:
                self.win.addstr(table_y, table_x, frame)
                if self.audio:
                    audio_controller.play_random_sound_print()
                self.win.refresh()
                time.sleep(self.delay)
                table_y += 1

            self.win.refresh()
            logger.info("Animation played")

    class loadingAnimation():
        def __init__(self, parent):
            self.parent = parent
            self.win = parent.win

            self.imports = [
                "controller.AudioController",
                "controller.LibController",
                "controller.InputController",
                "controller.MenuController",
                "lib.SaveManager",
                "lib.Logger",
                "lib.Consolas",
                "lib.SaveManager",
                "lib.Terminalium",
                "data.Config",
                "data.Player",
                "data.Ability",
                "data.Item",
                "data.Quest",
                "data.Skill",
                "data.Spell",
                "data.WorldValues",
            ]

            self.loading_animation()

        def loading_animation(self):
            animation_symbols = ['|', '/', '-', '\\']
            max_length = max(len(module) for module in self.imports)
            height, width = self.win.getmaxyx()
            y = 0

            for module in self.imports:
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
            logger.info("Loading animation completed")

    class Menu:
        def __init__(self, parent, title, options, additional_info=None, alignment="c", x=None, y=None, color='cyan', tips=True, clear=True, info_width=50, table_width=22, Xdo="=", Ydo="="):
            self.parent = parent
            self.config = parent.config
            self.win = parent.win
            self.option_handlers = options
            self.options = list(options.keys())

            if additional_info is None:
                additional_info = ["" for _ in options]
            self.title = title
            self.additional_info = additional_info
            self.alignment = alignment
            self.x = x
            self.y = y
            self.color = color
            self.tips = tips
            self.clear = clear
            self.info_width = info_width
            self.table_width = table_width
            self.Xdo = Xdo
            self.Ydo = Ydo

            self.menu_active = False
            self.menu_paused = True
            self.menu_thread = None
            self.is_first_display = True

            self.menu()

        def display_info(self, info_win, additional_info, option):
            color = 3 if self.menu_paused else 1
            info_win.attron(curses.color_pair(color))
            info_lines = additional_info[option].split('\n')
            for i, line in enumerate(info_lines, start=1):
                info_win.addstr(i, 1, line)
            info_win.attroff(curses.color_pair(color))

        def create_table(self, win, title, options, selected_index, table_width=22):
            main_color = 3 if self.menu_paused else 1
            selected_color = 3 if self.menu_paused else 2

            def separator_up_info():
                win.addstr("Xx" + "_" * (table_width + 2) + "xX\n", curses.color_pair(main_color))
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_sound_print()
                    win.refresh()

            def separator_center_info():
                win.addstr("||" + "-" * (table_width + 2) + "||\n", curses.color_pair(main_color))
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_sound_print()
                    win.refresh()

            def separator_down_info():
                win.addstr("Xx" + "¯" * (table_width + 2) + "xX\n", curses.color_pair(main_color))
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_sound_print()
                    win.refresh()

            separator_up_info()
            win.addstr("|| {:^{width}} ||\n".format(title, width=table_width), curses.color_pair(main_color))
            separator_center_info()

            for index, option in enumerate(options):
                if index == selected_index and not self.menu_paused:
                    option_str = "> {:<{width}}".format(option, width=table_width - 2)
                    win.addstr("|| ", curses.color_pair(main_color))
                    win.addstr(option_str, curses.color_pair(selected_color))
                    win.addstr(" ||\n", curses.color_pair(main_color))
                else:
                    option_str = "  {:<{width}}".format(option, width=table_width - 2)
                    win.addstr("|| ", curses.color_pair(main_color))
                    win.addstr(option_str, curses.color_pair(main_color))
                    win.addstr(" ||\n", curses.color_pair(main_color))

                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_sound_print()
                    win.refresh()

            separator_down_info()

        def menu(self):
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
            curses.init_pair(1, 7, bc)
            curses.init_pair(2, col[self.color], bc)
            curses.init_pair(3, 8, bc)

            if self.clear:
                self.win.clear()
                self.win.refresh()

            self.menu_x, self.menu_y = self.parent.calculate_position(30, len(self.options) + 5, self.alignment, self.x, self.y, self.Xdo, self.Ydo)

            menu_win = curses.newwin(len(self.options) + 5, 30, self.menu_y, self.menu_x)
            info_win = None
            if self.tips:
                self.info_x, self.info_y = self.menu_x + 35, self.menu_y
                info_win = curses.newwin(len(self.options) + 5, self.info_width, self.info_y, self.info_x)

            self.menu_active = True
            self.menu_thread = threading.Thread(target=self._menu_loop, args=(menu_win, info_win, self.title, self.options, self.additional_info, self.tips))
            self.menu_thread.start()

        def _menu_loop(self, menu_win, info_win, title, options, additional_info, tips):
            option = 0
            while self.menu_active:
                menu_win.erase()
                if tips:
                    info_win.erase()
                    box_color = curses.color_pair(3) if self.menu_paused else curses.color_pair(1)
                    info_win.attron(box_color)
                    info_win.box()
                    info_win.attroff(box_color)
                    self.display_info(info_win, additional_info, option)

                self.create_table(menu_win, title, self.options, option, self.table_width)
                menu_win.refresh()
                if tips:
                    info_win.refresh()

                if not self.menu_paused:
                    event = keyboard.read_event()
                    if event.event_type == keyboard.KEY_DOWN:
                        c = event.name
                        if c == 'up':
                            option = (option - 1) % len(self.options)
                            audio_controller.play_random_sound_print()
                        elif c == 'down':
                            option = (option + 1) % len(self.options)
                            audio_controller.play_random_sound_print()
                        elif c == 'enter':
                            selected_option = self.options[option]
                            self.option_handlers[selected_option]()
                            audio_controller.play_random_sound_print()
                            break
                else:
                    time.sleep(0.01)

                self.is_first_display = False

            self.menu_active = False


        def toggle_pause(self):
            self.menu_paused = not self.menu_paused
            if not self.menu_paused:
                self.menu()

        def stop_menu(self):
            self.menu_active = False
            if self.menu_thread:
                self.menu_thread.join()

    class TextBox():
        def __init__(self, parent, table_alignment="c", clear=True, x=None, y=None, width=22, max_sumbol=22, type="str", Xdo="=", Ydo="="):
            self.parent = parent
            self.config = parent.config
            self.win = parent.win
            self.is_first_display = True

            self.menu_y = 0
            self.menu_x = 0

            self.alignment = table_alignment
            self.x = x
            self.y = y
            self.clear = clear
            self.width = width
            self.max_sumbol = max_sumbol
            self.type = type
            self.Xdo = Xdo
            self.Ydo = Ydo

            self.paused = True

        def create_table_text_box(self, win, width):
            def separator_up_info():
                win.addstr(self.menu_y, self.menu_x, "Xx" + "_" * (width + 2) + "xX\n")
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_sound_print()
                    win.refresh()

            def separator_down_info():
                win.addstr(self.menu_y + 2, self.menu_x , "Xx" + "¯" * (width + 2) + "xX\n")
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_sound_print()
                    win.refresh()

            separator_up_info()
            win.addstr(self.menu_y + 1, self.menu_x, "||" + " " * (width + 2) + "||")
            if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_sound_print()
                    win.refresh()
            separator_down_info()

            return [self.menu_x + 3, self.menu_y + 1]

        def text_box(self):
            if self.clear:
                self.win.clear()
                self.win.refresh()

            self.menu_x, self.menu_y = self.parent.calculate_position(
                self.width+7, 3, self.alignment, x=self.x, y=self.y, Xdo=self.Xdo, Ydo=self.Ydo)

            c_position = self.create_table_text_box(self.win, self.width)
            self.win.move(c_position[1], c_position[0])

            text = ""
            while True:
                event = keyboard.read_event()

                if event.event_type != keyboard.KEY_DOWN:
                    continue

                key = event.name

                if key == 'backspace':
                    if len(text) > 0:
                        text = text[:-1]
                        self.win.move(c_position[1], c_position[0] + len(text))
                        self.win.addstr(' ')
                        audio_controller.play_random_sound_print()

                elif key == 'enter':
                    self.win.clear()
                    self.win.refresh()
                    audio_controller.play_random_sound_print()
                    break

                else:
                    validators = {
                        "str": lambda k: k.isprintable() or k == 'space',
                        "int": lambda k: k.isdigit() or k.startswith('numpad'),
                        "float": lambda k: k.isdigit() or k in {'.', ','} or k.startswith('numpad')
                    }

                    char = None
                    if key == 'space':
                        char = ' '
                    elif key.startswith('numpad'):
                        if key == 'numpad decimal':
                            char = '.' if self.type == 'float' else None
                        else:
                            char = key.replace('numpad ', '')
                    elif len(key) == 1:
                        char = key.upper() if keyboard.is_pressed('shift') else key

                    if char and validators.get(self.type, lambda _: False)(char):
                        if len(text) < self.max_sumbol:
                            if self.type == 'float':
                                if char == ',':
                                    char = '.'
                                if char == '.' and '.' in text:
                                    continue
                            
                            text += char
                            audio_controller.play_random_sound_print()

                self.win.move(c_position[1], c_position[0])
                self.win.addstr(text.ljust(self.max_sumbol))
                self.win.refresh()

                self.is_first_display = False

            self.is_first_display = True
            return text


        def toggle_pause(self):
            self.paused = not self.paused
            if not self.paused:
                self.text_box()
