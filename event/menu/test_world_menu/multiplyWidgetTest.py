from controller.LibController import lib_controller
from controller.MenuController import menu_controller

class multiplyWidgetTest():
    def __init__(self):
        self.consolas = lib_controller.consolas
        self.tab_control = False

        self.main_menu = None
        self.main_menu1 = None
        self.main_menu2 = None

    def run(self):

        self.main_menu = self.consolas.create_menu(
            clear=True,
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

        if not self.tab_control:
            self.widgets_list = [self.main_menu, self.main_menu1]
            self.consolas.start_tab_control(self.widgets_list)
            self.tab_control = True

    def option(self):
        self.main_menu.stop_menu()
        self.main_menu1.stop_menu()
        menu_controller.show_main_menu()





multiply_widget_test = multiplyWidgetTest()