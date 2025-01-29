import dearpygui.dearpygui as dpg
from lib.Logger import logger

class Terminalium():
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.log_text = ""
        self.command_history = []
        self.history_index = 0

    def exit_terminalium(self):
        dpg.stop_dearpygui()

    def execute_command(self, sender, app_data, user_data):
        command = dpg.get_value("command_input")
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.log_text += f"> {command}\n"



        self.log_text += f"Entar comand: {command}\n"
        dpg.set_value("log_output", self.log_text)
        dpg.set_value("command_input", "")

    def handle_key_press(self, sender, app_data):
        if app_data == dpg.mvKey_Up:
            if self.history_index > 0:
                self.history_index -= 1
                dpg.set_value("command_input", self.command_history[self.history_index])
        elif app_data == dpg.mvKey_Down:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                dpg.set_value("command_input", self.command_history[self.history_index])
            elif self.history_index == len(self.command_history) - 1:
                self.history_index += 1
                dpg.set_value("command_input", "")

    def show_terminal(self):
        logger.info("Showing terminalium")

        dpg.create_context()

        with dpg.window(label="Terminalium", width=self.window_width, height=self.window_height, tag="terminalium"):
            with dpg.group(horizontal=False):
                dpg.add_input_text(multiline=True, readonly=True, width=-1, height=-50, tag="log_output")
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="", tag="command_input", width=-50)
                    dpg.add_button(label="Enter", callback=self.execute_command)

        dpg.set_primary_window("terminalium", True)
        
        with dpg.handler_registry():
            dpg.add_key_press_handler(callback=self.handle_key_press)

        dpg.create_viewport(title="Terminalium", width=self.window_width, height=self.window_height)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

terminalium = Terminalium()