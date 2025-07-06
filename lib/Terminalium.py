import dearpygui.dearpygui as dpg
from lib.Logger import logger
from inspect import signature
from Assets.controller.MenuController import menu_controller

class Terminalium():
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.log_text = ""
        self.command_history = []
        self.history_index = 0
        self.commands = {}
        self.font_size = 18

        self.register_command("help", self._cmd_help, "Show list of commands")
        self.register_command("exit", self._cmd_exit, "Close Terminalium")
        self.register_command("menu", self._switch_menu, "Switch room: menu <name>")

    def _switch_menu(self, room_name):
        if room_name == "audio_test_menu" or room_name == "audio_test"  or room_name == "atm":
            menu_controller.show_audio_test_menu()
        elif room_name == "main_menu" or room_name == "main" or room_name == "mm":
            menu_controller.show_main_menu()
        elif room_name == "autors_menu" or room_name == "autors" or room_name == "am":
            menu_controller.show_autors_menu()
        elif room_name == "widget_test_menu" or room_name == "widget_test" or room_name == "wtm":
            menu_controller.show_widget_test_menu()

    def register_command(self, name, callback, description=""):
        self.commands[name] = {
            "callback": callback,
            "description": description,
            "args": list(signature(callback).parameters.keys())
        }

    def _cmd_help(self):
        help_text = "Available commands:\n"
        for cmd, data in self.commands.items():
            args = " ".join([f"<{arg}>" for arg in data["args"]])
            help_text += f"{cmd} {args} - {data['description']}\n"
        self.log_text += help_text

    def _cmd_exit(self):
        self.exit_terminalium()

    def exit_terminalium(self):
        dpg.stop_dearpygui()

    def _parse_input(self, input_str):
        parts = input_str.strip().split()
        if not parts:
            return None, []
        cmd = parts[0]
        args = parts[1:]
        return cmd, args

    def execute_command(self, sender, app_data, user_data):
        command_input = dpg.get_value("command_input")
        if not command_input:
            return

        self.command_history.append(command_input)
        self.history_index = len(self.command_history)
        self.log_text += f"> {command_input}\n"

        cmd_name, args = self._parse_input(command_input)
        
        if cmd_name in self.commands:
            try:
                self.commands[cmd_name]["callback"](*args)
            except Exception as e:
                self.log_text += f"Error: {str(e)}\n"
        else:
            self.log_text += f"Command '{cmd_name}' not found. Type 'help' for a list of commands.\n"

        dpg.set_value("log_output", self.log_text)
        dpg.set_value("command_input", "")
        dpg.focus_item("command_input")
        dpg.configure_item("log_output", tracked=True)

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
        elif app_data == dpg.mvKey_Return:
            self.execute_command(None, None, None)

    def show_terminal(self):
        logger.info("Showing terminalium")

        dpg.create_context()

        with dpg.font_registry():
            default_font = dpg.add_font("C:/Windows/Fonts/segoeui.ttf", 23)

        dpg.bind_font(default_font)

        with dpg.window(label="Terminalium", width=self.window_width, height=self.window_height, tag="terminalium"):
            with dpg.group(horizontal=False):
                dpg.add_input_text(multiline=True, readonly=True, width=-1, height=-50, tag="log_output", tracked=True)
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="", tag="command_input", width=-50, on_enter=True)
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