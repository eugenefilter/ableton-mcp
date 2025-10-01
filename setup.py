
import os
import shutil
import subprocess

# --- Конфигурация ---
SOURCE_DIR = "MyAgent"
DEST_DIR_PARENT = "/Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts"
DEST_DIR = os.path.join(DEST_DIR_PARENT, "MyAgent")

def copy_script():
    """Копирует скрипт в папку Ableton."""
    print(f"Исходная директория: {os.path.abspath(SOURCE_DIR)}")

    print(f"Целевая директория: {DEST_DIR}")

    if not os.path.exists(SOURCE_DIR):
        print(f"ОШИБКА: Исходная директория '{SOURCE_DIR}' не найдена.")
        return False

    try:
        # Создаем родительскую директорию, если ее нет
        if not os.path.exists(DEST_DIR_PARENT):
            print(f"Создаю директорию: {DEST_DIR_PARENT}")
            os.makedirs(DEST_DIR_PARENT)

        # Удаляем старую версию скрипта, если она есть
        if os.path.exists(DEST_DIR):
            print("Удаляю предыдущую версию скрипта...")
            shutil.rmtree(DEST_DIR)

        # Копируем новую версию
        print("Копирую файлы скрипта...")
        shutil.copytree(SOURCE_DIR, DEST_DIR)
        print("\nСКРИПТ УСПЕШНО СКОПИРОВАН!\n")
        return True

    except Exception as e:
        print(f"\nОШИБКА КОПИРОВАНИЯ: {e}")
        print("Пожалуйста, попробуйте скопировать папку 'MyAgent' вручную.")
        return False

if __name__ == "__main__":
    if copy_script():
        print("Теперь перезапустите Ableton Live, чтобы он обнаружил скрипт.")
        print("Затем выберите 'MyAgent' в настройках 'Link/MIDI'.")