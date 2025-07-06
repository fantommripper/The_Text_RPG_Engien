from controller.LibController import LibController
from controller.MenuController import menu_controller

class multiplyWidgetTest():
    def __init__(self):
        self.consolas = LibController.get_instance().consolas
        self.text = None
        self.main_menu = None
        self.main_menu1 = None
        self.main_menu2 = None

    def run(self):
        self.textBox = self.consolas.create_text_box(
            function=self.textBoxOption,
            Ydo="-",
            y=10,
        )

        self.main_menu = self.consolas.create_menu(
            clear=False,
            title="Menu",
            options={"1" : self.option, "2" : self.option},
            tips=False
        )

        self.main_menu1 = self.consolas.create_menu(
            clear=False,
            title="Menu1",
            options={"1" : self.option, "2" : self.option},
            Xdo="-",
            x=40,
            tips=False
        )

        self.main_menu2 = self.consolas.create_menu(
            clear=False,
            title="Menu2",
            options={"1" : self.option, "2" : self.option},
            Xdo="+",
            x=40,
            tips=False
        )

    def option(self):
        if self.main_menu:
            self.main_menu.stop()
        if self.main_menu1:
            self.main_menu1.stop()
        if self.main_menu2:
            self.main_menu2.stop()
        if self.textBox:
            self.textBox.stop()
        menu_controller.show_main_menu()

    def textBoxOption(self, A):
        if self.main_menu:
            self.main_menu.stop()
        if self.main_menu1:
            self.main_menu1.stop()
        if self.main_menu2:
            self.main_menu2.stop()
        if self.textBox:
            self.textBox.stop()
        menu_controller.show_main_menu()

multiply_widget_test = multiplyWidgetTest()