import sys
import os
import importlib
import traceback

def run_game():
    # Получаем путь к текущей папке (Assets)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Получаем корневую папку проекта (на уровень выше Assets)
    project_root = os.path.dirname(current_dir)
    
    # Добавляем корневую папку проекта в sys.path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        print(f"Added project root path: {project_root}")
    
    # Добавляем папку Assets в sys.path (для main.py)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        print(f"Added Assets path: {current_dir}")
    
    try:
        # Импортируем main из текущей папки (Assets)
        import main
        print("Successfully imported main module")
        
        # Запускаем игру
        main.main()
    except ImportError as e:
        print(f"Failed to import main module: {e}")
        print("Current sys.path:")
        for path in sys.path:
            print(f"  - {path}")
        with open("bootstrap_error.log", "w", encoding="utf-8") as f:
            f.write("ImportError: " + str(e) + "\n")
            f.write(traceback.format_exc())
        raise
    except Exception as e:
        print(f"Error running game: {e}")
        with open("bootstrap_error.log", "w", encoding="utf-8") as f:
            f.write("Exception: " + str(e) + "\n")
            f.write(traceback.format_exc())
        raise

if __name__ == '__main__':
    run_game()