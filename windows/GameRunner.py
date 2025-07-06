import dearpygui.dearpygui as dpg
import os
import subprocess
import sys
import threading
import time
from lib.Logger import logger

class GameRunner:
    def __init__(self):
        self.window_id = None
        self.assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets")
        self.main_py_path = os.path.join(self.assets_path, "main.py")
        self.bootstrap_path = os.path.join(self.assets_path, "bootstrap.py")
        self.game_process = None
        self.is_game_running = False

    def show(self):
        if self.window_id and dpg.does_item_exist(self.window_id):
            dpg.show_item(self.window_id)
            return

        self._create_window()

    def _create_window(self):
        with dpg.window(label="Game Runner", width=500, height=600, pos=[50, 300]) as self.window_id:
            dpg.add_text("Game Launcher")
            dpg.add_separator()

            # Информация о игре
            with dpg.group():
                dpg.add_text("Game Status:", color=[100, 200, 255])
                dpg.add_text("Ready to launch", tag="game_status", color=[100, 255, 100])

                dpg.add_separator()

                dpg.add_text("Assets Path:")
                dpg.add_text(self.assets_path, wrap=450, color=[200, 200, 200])
                
                dpg.add_text("Main.py Path:")
                dpg.add_text(self.main_py_path, wrap=450, color=[200, 200, 200])

                dpg.add_text("Bootstrap.py Path:")
                dpg.add_text(self.bootstrap_path, wrap=450, color=[200, 200, 200])

                # Проверяем существование файлов
                if os.path.exists(self.main_py_path):
                    dpg.add_text("[Y] main.py found", color=[100, 255, 100])
                else:
                    dpg.add_text("[N] main.py not found!", color=[255, 100, 100])
                
                if os.path.exists(self.bootstrap_path):
                    dpg.add_text("[Y] bootstrap.py found", color=[100, 255, 100])
                else:
                    dpg.add_text("[N] bootstrap.py not found!", color=[255, 100, 100])

                # Проверяем lib папку
                lib_path = os.path.join(os.path.dirname(self.assets_path), "lib")
                if os.path.exists(lib_path):
                    dpg.add_text("[Y] lib folder found", color=[100, 255, 100])
                else:
                    dpg.add_text("[N] lib folder not found!", color=[255, 100, 100])
            
            dpg.add_separator()
            
            # Кнопки управления
            with dpg.group():
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Launch Game",
                        callback=self._launch_game,
                        width=120,
                        height=40,
                        tag="launch_btn"
                    )
                    dpg.add_button(
                        label="Stop Game",
                        callback=self._stop_game,
                        width=120,
                        height=40,
                        tag="stop_btn",
                        enabled=False
                    )
                
                dpg.add_separator()
                
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Open Game Folder",
                        callback=self._open_game_folder,
                        width=150
                    )
                    dpg.add_button(
                        label="Refresh Status",
                        callback=self._refresh_status,
                        width=120
                    )
                    dpg.add_button(
                        label="Test Bootstrap",
                        callback=self._test_bootstrap,
                        width=120
                    )
            
            dpg.add_separator()
            
            # Лог вывод
            with dpg.collapsing_header(label="Game Output Log"):
                with dpg.child_window(height=-1, width=-1, tag="game_log_container"):
                    dpg.add_text("Game output will appear here...", tag="game_log", wrap=450)

    def _test_bootstrap(self):
        """Тестирует bootstrap в отдельном процессе с выводом в лог"""
        if not os.path.exists(self.bootstrap_path):
            self._show_error_dialog(f"Bootstrap file not found: {self.bootstrap_path}")
            return
        
        try:
            self._add_log("Testing bootstrap script...")
            
            # Запускаем bootstrap с захватом вывода
            result = subprocess.run(
                [sys.executable, self.bootstrap_path],
                cwd=self.assets_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            self._add_log(f"Bootstrap exit code: {result.returncode}")
            
            if result.stdout:
                self._add_log(f"STDOUT:\n{result.stdout}")
            
            if result.stderr:
                self._add_log(f"STDERR:\n{result.stderr}")
                
        except subprocess.TimeoutExpired:
            self._add_log("Bootstrap test timed out (10 seconds)")
        except Exception as e:
            self._add_log(f"Bootstrap test error: {e}")

    def _launch_game(self):
        """Запускает игру"""
        if self.is_game_running:
            self._show_error_dialog("Game is already running!")
            return

        if not os.path.exists(self.bootstrap_path):
            self._show_error_dialog(f"Bootstrap file not found: {self.bootstrap_path}")
            return
        
        if not os.path.exists(self.main_py_path):
            self._show_error_dialog(f"Main file not found: {self.main_py_path}")
            return
        
        try:
            logger.info("Launching game...")
            self._update_status("Launching game...", [255, 255, 100])
            self._add_log("Starting game launch process...")

            # Обновляем состояние кнопок
            self.is_game_running = True
            self._update_buttons(launch_enabled=False, stop_enabled=True)

            # Формируем команду с добавлением пути к библиотекам
            if sys.platform.startswith('win'):
                self.game_process = subprocess.Popen(
                    [sys.executable, self.bootstrap_path],
                    cwd=self.assets_path,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                if sys.platform == 'darwin':
                    cmd = ['osascript', '-e', f'tell app "Terminal" to do script "cd {self.assets_path} && python3 {self.bootstrap_path}"']
                else:
                    cmd = ['gnome-terminal', '--', 'bash', '-c', f'cd {self.assets_path} && python3 {self.bootstrap_path}; read']
                
                self.game_process = subprocess.Popen(cmd)
            
            self._update_status("Game is running", [100, 255, 100])
            self._add_log("Game launched successfully")
            
            # Запускаем мониторинг процесса в отдельном потоке
            monitor_thread = threading.Thread(target=self._monitor_game_process)
            monitor_thread.daemon = True
            monitor_thread.start()
            
        except Exception as e:
            logger.error(f"Error launching game: {e}")
            self._show_error_dialog(f"Failed to launch game: {str(e)}")
            self._update_status("Launch failed", [255, 100, 100])
            self.is_game_running = False
            self._update_buttons(launch_enabled=True, stop_enabled=False)
            self._add_log(f"Launch failed: {e}")

    def _stop_game(self):
        """Останавливает игру"""
        if not self.is_game_running or not self.game_process:
            self._show_error_dialog("No game process to stop!")
            return
        
        try:
            logger.info("Stopping game...")
            self._update_status("Stopping game...", [255, 255, 100])
            self._add_log("Stopping game process...")
            
            # Завершаем процесс
            self.game_process.terminate()
            
            # Ждем завершения с таймаутом
            try:
                self.game_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Принудительно убиваем процесс
                self.game_process.kill()
                self._add_log("Game process forcefully terminated")
            
            self.is_game_running = False
            self.game_process = None
            self._update_status("Game stopped", [255, 200, 100])
            self._update_buttons(launch_enabled=True, stop_enabled=False)
            self._add_log("Game stopped")
            
        except Exception as e:
            logger.error(f"Error stopping game: {e}")
            self._show_error_dialog(f"Failed to stop game: {str(e)}")

    def _monitor_game_process(self):
        """Мониторит процесс игры"""
        while self.is_game_running and self.game_process:
            try:
                # Проверяем, жив ли процесс
                return_code = self.game_process.poll()
                if return_code is not None:
                    # Процесс завершился
                    self.is_game_running = False
                    self.game_process = None
                    
                    if return_code == 0:
                        self._update_status("Game finished normally", [100, 255, 100])
                        self._add_log("Game finished normally")
                    else:
                        self._update_status(f"Game crashed (code: {return_code})", [255, 100, 100])
                        self._add_log(f"Game crashed with exit code: {return_code}")
                    
                    self._update_buttons(launch_enabled=True, stop_enabled=False)
                    break
                
                time.sleep(1)  # Проверяем каждую секунду
                
            except Exception as e:
                logger.error(f"Error monitoring game process: {e}")
                break

    def _open_game_folder(self):
        """Открывает папку с игрой в файловом менеджере"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(self.assets_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', self.assets_path])
            else:  # Linux
                subprocess.run(['xdg-open', self.assets_path])
        except Exception as e:
            logger.error(f"Error opening game folder: {e}")
            self._show_error_dialog(f"Failed to open folder: {str(e)}")

    def _refresh_status(self):
        """Обновляет статус игры"""
        if os.path.exists(self.main_py_path) and os.path.exists(self.bootstrap_path):
            if self.is_game_running:
                self._update_status("Game is running", [100, 255, 100])
            else:
                self._update_status("Ready to launch", [100, 255, 100])
        else:
            self._update_status("Game files not found", [255, 100, 100])
        
        self._add_log("Status refreshed")

    def _update_status(self, message, color):
        """Обновляет статус игры"""
        if dpg.does_item_exist("game_status"):
            dpg.set_value("game_status", message)
            dpg.configure_item("game_status", color=color)

    def _update_buttons(self, launch_enabled, stop_enabled):
        """Обновляет состояние кнопок"""
        if dpg.does_item_exist("launch_btn"):
            dpg.configure_item("launch_btn", enabled=launch_enabled)
        if dpg.does_item_exist("stop_btn"):
            dpg.configure_item("stop_btn", enabled=stop_enabled)

    def _add_log(self, message):
        """Добавляет сообщение в лог"""
        if dpg.does_item_exist("game_log"):
            current_log = dpg.get_value("game_log")
            timestamp = time.strftime("%H:%M:%S")
            new_log = f"[{timestamp}] {message}\n{current_log}"
            
            # Ограничиваем размер лога
            lines = new_log.split('\n')
            if len(lines) > 50:  # Максимум 50 строк
                new_log = '\n'.join(lines[:50])
            
            dpg.set_value("game_log", new_log)

    def _show_error_dialog(self, message):
        """Показывает диалог ошибки"""
        if dpg.does_item_exist("game_error_dialog"):
            dpg.delete_item("game_error_dialog")
            
        with dpg.window(label="Error", modal=True, width=400, height=150, tag="game_error_dialog"):
            dpg.add_text(message, wrap=370, color=[255, 100, 100])
            dpg.add_separator()
            dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item("game_error_dialog"))

    def cleanup(self):
        """Очистка ресурсов при закрытии"""
        if self.is_game_running and self.game_process:
            try:
                self.game_process.terminate()
                self.game_process.wait(timeout=3)
            except:
                try:
                    self.game_process.kill()
                except:
                    pass