from controller.LibController import lib_controller

class multiplyWidgetTest():
    def __init__(self):
        self.consolas = lib_controller.consolas
        self.tab_control = False

        self.main_menu = None
        self.main_menu1 = None
        self.main_menu2 = None

    def run(self):
        while True:
            self.main_menu = self.consolas.create_menu(
                clear=True,
                title="Menu",
                options=["1","2"],
                tips=False
            )
            self.main_menu1 = self.consolas.create_menu(
                clear=False,
                title="Menu1",
                options=["1","2"],
                Xdo="-",
                x=40,
                tips=False
            )
            self.main_menu2 = self.consolas.create_text_box(
                clear=False,
                Xdo="+",
                x=40,
            )


            if not self.tab_control:
                self.widgets_list = [self.main_menu, self.main_menu1, self.main_menu2]
                self.consolas.start_tab_control(self.widgets_list)
                self.tab_control = True

            self.action = self.main_menu.get_menu_result()
            self.action1 = self.main_menu1.get_menu_result()
            self.action2 = self.main_menu2.get_menu_result()





multiply_widget_test = multiplyWidgetTest()