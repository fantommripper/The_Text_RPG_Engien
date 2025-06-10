from typing import List, Dict

from controller.LibController import lib_controller

from lib.widgets.MenuWidget import MenuWidget
from lib.widgets.TextBoxWidget import TextBoxWidget
from lib.widgets.TableWidget import TableWidget
from lib.widgets.FastLoadingWidget import FastLoadingWidget
from lib.widgets.AnimationWidget import AnimationWidget
from lib.widgets.LoadingAnimationWidget import LoadingAnimationWidget

from lib.Logger import logger

class Consolas:
    def __init__(self, config, player, win):
        self.config = config
        self.player = player
        self.win = win
        self.current_focus = 0

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

    def fast_loading(self, speed=0.04) -> FastLoadingWidget:
        return FastLoadingWidget(self, speed)

    def create_table(self, *args:str, style:str = "info", clear:bool = True, separator_positions:List[int]=None,
                    textAlignment:Dict[int, str] = None, tableAlignment:str = "c", width:int = 22, x:int = None, y:int = None,
                    Xdo:str = "=", Ydo:str = "=", animation:bool = True) -> TableWidget:
        return TableWidget(self, *args, style=style, clear=clear, separator_positions=separator_positions,
                        textAlignment=textAlignment, tableAlignment=tableAlignment, width=width,
                        x=x, y=y, Xdo=Xdo, Ydo=Ydo, animation=animation)

    def play_animation(self, frames, delay=0.3, alignmentTable="c", x=None, y=None, clear=True, Xdo="=", Ydo="=", audio=True) -> AnimationWidget:
        return AnimationWidget(self, frames, delay, alignmentTable, x, y, clear, Xdo, Ydo, audio)

    def loading_animation(self) -> LoadingAnimationWidget:
        return LoadingAnimationWidget(self)

    def create_menu(self, title:str, options:List[str], additional_info=None,
                    alignment="c", x:int=None, y:int=None, color='cyan',
                    tips=True, clear=True, info_width=50, table_width=22,
                    Xdo="=", Ydo="=") -> MenuWidget:
        return MenuWidget(self, title, options, additional_info, alignment, x, y, color, tips, clear, info_width, table_width, Xdo, Ydo)

    def create_text_box(self, table_alignment="c", clear=True, x=None, y=None, width=22, max_symbol=22, input_type="str", Xdo="=", Ydo="=", function=None) -> TextBoxWidget:
        return TextBoxWidget(self, table_alignment, clear, x, y, width, max_symbol, input_type, Xdo, Ydo, function)
