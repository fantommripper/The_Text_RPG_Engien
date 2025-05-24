import curses
import curses.ascii
import time
import random as r

import keyboard

from controller.AudioController import audio_controller
from controller.LibController import lib_controller

from lib.Logger import logger

class Consolas:
    def __init__(self, config, player, win):
        self.config = config
        self.player = player
        self.win = win
        self.current_focus = 0
        self.input_controller = lib_controller.input_controller

        self.tab_input_event = None
        self.btab_input_event = None

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

    def create_text_box(self, table_alignment="c", clear=True, x=None, y=None, width=22, max_sumbol=22, input_type="str", Xdo="=", Ydo="=", function=None):
        return self.TextBox(self, table_alignment, clear, x, y, width, max_sumbol, input_type, Xdo, Ydo, function)

    #——————————————————————————————tab control——————————————————————————————

    def start_tab_control(self, widgets: list):
        self.current_focus = 0
        self.widgets = widgets
        self.widgets[self.current_focus].toggle_pause()

        curses.mousemask(1)

        self.tab_input_event = self.input_controller.add_input_event(curses.ascii.TAB, self.next_widget)
        self.btab_input_event = self.input_controller.add_input_event(curses.KEY_BTAB, self.preceding_widget)

    def next_widget(self):
        self.widgets[self.current_focus].toggle_pause()

        self.current_focus = (self.current_focus + 1) % len(self.widgets)
        audio_controller.play_random_print_sound()

        self.widgets[self.current_focus].toggle_pause()

    def preceding_widget(self):
        self.widgets[self.current_focus].toggle_pause()

        self.current_focus = (self.current_focus - 1) % len(self.widgets)
        audio_controller.play_random_print_sound()

        self.widgets[self.current_focus].toggle_pause()

    def stop_tab_control(self):
        self.input_controller.remove_input_event(self.tab_input_event)
        self.input_controller.remove_input_event(self.btab_input_event)
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

            audio_controller.play_random_print_sound()
            self.win.refresh()
            logger.info("Table created")

        def _draw_table_header(self):
            if self.style == "info":
                self._separator_up_info()
            elif self.style == "error":
                self._separator_up_error()

            audio_controller.play_random_print_sound()
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
                audio_controller.play_random_print_sound()
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
                    audio_controller.play_random_print_sound()
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
            self.input_controller = parent.input_controller
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

            self.input_event_up_id = None
            self.input_event_down_id = None
            self.input_event_enter_id = None

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
                    audio_controller.play_random_print_sound()
                    win.refresh()

            def separator_center_info():
                win.addstr("||" + "-" * (table_width + 2) + "||\n", curses.color_pair(main_color))
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_print_sound()
                    win.refresh()

            def separator_down_info():
                win.addstr("Xx" + "¯" * (table_width + 2) + "xX\n", curses.color_pair(main_color))
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_print_sound()
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
                    audio_controller.play_random_print_sound()
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
            curses.init_pair(1, curses.COLOR_WHITE, bc)
            curses.init_pair(2, col[self.color], bc)
            curses.init_pair(3, curses.COLOR_WHITE, bc)

            if self.clear:
                self.win.clear()
                self.win.refresh()

            self.menu_x, self.menu_y = self.parent.calculate_position(30, len(self.options) + 5, self.alignment, self.x, self.y, self.Xdo, self.Ydo)

            self.menu_win = curses.newwin(len(self.options) + 5, 30, self.menu_y, self.menu_x)
            self.info_win = None
            if self.tips:
                self.info_x, self.info_y = self.menu_x + 35, self.menu_y
                self.info_win = curses.newwin(len(self.options) + 5, self.info_width, self.info_y, self.info_x)

            self.menu_active = True
            self.option = 0
            self._update_menu()

            self.input_event_up_id = self.input_controller.add_input_event(curses.KEY_UP, self._option_up)
            self.input_event_down_id = self.input_controller.add_input_event(curses.KEY_DOWN, self._option_down)
            self.input_event_enter_id = [
                self.input_controller.add_input_event(curses.KEY_ENTER, self._option_enter),
                self.input_controller.add_input_event(10, self._option_enter),
                self.input_controller.add_input_event(13, self._option_enter)
            ]

        def _update_menu(self):
            self.menu_win.erase()
            if self.tips:
                self.info_win.erase()
                box_color = curses.color_pair(3) if self.menu_paused else curses.color_pair(1)
                self.info_win.attron(box_color)
                self.info_win.box()
                self.info_win.attroff(box_color)
                self.display_info(self.info_win, self.additional_info, self.option)

            self.create_table(self.menu_win, self.title, self.options, self.option, self.table_width)
            self.menu_win.refresh()
            if self.tips:
                self.info_win.refresh()
            self.is_first_display = False

        def _option_up(self):
            self.option = (self.option - 1) % len(self.options)
            audio_controller.play_random_print_sound()

            self._update_menu()

        def _option_down(self):
            self.option = (self.option + 1) % len(self.options)
            audio_controller.play_random_print_sound()

            self._update_menu()

        def _option_enter(self):
            selected_option = self.options[self.option]
            self.option_handlers[selected_option]()
            audio_controller.play_random_print_sound()

            self._update_menu()


        def toggle_pause(self):
            self.menu_paused = not self.menu_paused
            self._update_menu()
            self.input_controller.set_input_event_pause(self.input_event_up_id, self.menu_paused)
            self.input_controller.set_input_event_pause(self.input_event_down_id, self.menu_paused)

            for eid in self.input_event_enter_id:
                self.input_controller.set_input_event_pause(eid, self.menu_paused)

            if not self.menu_paused:
                curses.curs_set(0)

        def stop(self):
            self.menu_active = False
            self._update_menu()
            self.input_controller.remove_input_event(self.input_event_up_id)
            self.input_controller.remove_input_event(self.input_event_down_id)
            for eid in self.input_event_enter_id:
                self.input_controller.remove_input_event(eid)

    class TextBox():
        def __init__(self, parent, table_alignment="c", clear=True, x=None, y=None, width=22, max_sumbol=22, type="str", Xdo="=", Ydo="=", function=None):
            self.parent = parent
            self.config = parent.config
            self.win = parent.win
            self.input_controller = parent.input_controller
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
            self.function = function

            self._text = ""
            self._done = False
            self._input_event_ids = []

            self._c_position = None

            self.text_box()

        def create_table_text_box(self, win, width):
            def separator_up_info():
                win.addstr(self.menu_y, self.menu_x, "Xx" + "_" * (width + 2) + "xX\n")
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_print_sound()
                    win.refresh()

            def separator_down_info():
                win.addstr(self.menu_y + 2, self.menu_x , "Xx" + "¯" * (width + 2) + "xX\n")
                if self.is_first_display:
                    time.sleep(self.config.delayOutput)
                    audio_controller.play_random_print_sound()
                    win.refresh()

            separator_up_info()
            win.addstr(self.menu_y + 1, self.menu_x, "||" + " " * (width + 2) + "||")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                audio_controller.play_random_print_sound()
                win.refresh()
            separator_down_info()

            return [self.menu_x + 3, self.menu_y + 1]

        def _on_key(self, key):
            if self.paused:
                return

            if key in (curses.KEY_ENTER, 10, 13):
                self._done = True
                self.win.clear()
                self.win.refresh()
                audio_controller.play_random_print_sound()

                for eid in self._input_event_ids:
                    self.input_controller.remove_input_event(eid)

                self.is_first_display = True

                if self.function:
                    self.function(self._text)
                return

            elif key in (curses.KEY_BACKSPACE, 127, 8, 263):
                if len(self._text) > 0:
                    self._text = self._text[:-1]
                    audio_controller.play_random_print_sound()
            elif 32 <= key <= 126:
                char = chr(key)
                if self.type == "int" and not char.isdigit():
                    return
                if self.type == "float" and not (char.isdigit() or char in ".,"):
                    return
                if len(self._text) < self.max_sumbol:
                    if self.type == "float" and char == ',':
                        char = '.'
                    if self.type == "float" and char == '.' and '.' in self._text:
                        return
                    self._text += char
                    audio_controller.play_random_print_sound()

            self.win.move(self._c_position[1], self._c_position[0])
            self.win.addstr(self._text.ljust(self.max_sumbol))
            self.win.move(self._c_position[1], self._c_position[0] + len(self._text))
            self.win.refresh()

        def text_box(self):
            if self.clear:
                self.win.clear()
                self.win.refresh()

            curses.curs_set(1)

            self.menu_x, self.menu_y = self.parent.calculate_position(
                self.width+7, 3, self.alignment, x=self.x, y=self.y, Xdo=self.Xdo, Ydo=self.Ydo)

            self._c_position = self.create_table_text_box(self.win, self.width)
            self.win.move(self._c_position[1], self._c_position[0])

            self._text = ""
            self._done = False

            self._input_event_ids = []
            for k in list(range(32, 127)) + [curses.KEY_ENTER, 10, 13, curses.KEY_BACKSPACE, 127, 8]:
                eid = self.input_controller.add_input_event(k, lambda k=k: self._on_key(k))
                self._input_event_ids.append(eid)

        def toggle_pause(self):
            self.paused = not self.paused
            for eid in self._input_event_ids:
                self.input_controller.set_input_event_pause(eid, self.paused)
            if not self.paused:
                curses.curs_set(1)

        def stop(self):
            self._done = True
            for eid in self._input_event_ids:
                self.input_controller.remove_input_event(eid)
            self.is_first_display = True