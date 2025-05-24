from controller.LibController import lib_controller
from controller.MenuController import menu_controller

from lib.Logger import logger

class multiplyWidgetTest():
    def __init__(self):
        self.consolas = lib_controller.consolas
        self.tab_control = False

        self.textBox = None
        self.main_menu = None
        self.main_menu1 = None
        self.main_menu2 = None

    def run(self):
        self.textBox = self.consolas.create_text_box(function=self.textBoxOption, Ydo="-", y=10)

        self.main_menu = self.consolas.create_menu(
            clear=False,
            title="Menu",
            options={"1" : self.option,"2" : self.option},
            tips=False
        )

        self.main_menu1 = self.consolas.create_menu(
            clear=False,
            title="Menu1",
            options={"1" : self.option,"2" : self.option},
            Xdo="-",
            x=40,
            tips=False
        )

        self.main_menu2 = self.consolas.create_menu(
            clear=False,
            title="Menu2",
            options={"1" : self.option,"2" : self.option},
            Xdo="+",
            x=40,
            tips=False
        )

        if not self.tab_control:
            self.widgets_list = [self.textBox, self.main_menu1, self.main_menu, self.main_menu2]
            self.consolas.start_tab_control(self.widgets_list)
            self.tab_control = True

    def option(self):
        self.main_menu.stop()
        self.main_menu1.stop()
        self.main_menu2.stop()
        self.textBox.stop()
        menu_controller.show_main_menu()

    def textBoxOption(self, A):
        self.main_menu.stop()
        self.main_menu1.stop()
        self.main_menu2.stop()
        self.textBox.stop()
        menu_controller.show_main_menu()

multiply_widget_test = multiplyWidgetTest()