import os
import re
from datetime import datetime
from pathlib import Path

from print_utils import *

filename_date_format = "%Y-%m-%d_%H-%M-%S"


def get_creation_date(filepath) -> datetime:
    try:
        stat = os.stat(filepath)

        import platform
        if platform.system() == 'Darwin':  # macOS
            return datetime.fromtimestamp(stat.st_birthtime)

        # Linux, Windows
        return datetime.fromtimestamp(stat.st_ctime)
    except Exception as e:
        print(f"Ошибка при получении даты создания: {e}")
        return None


def filename_from_date(date: datetime, for_path: str = "", ext: str = "") -> str:
    new_name = date_name = date.strftime(filename_date_format)
    if not for_path:
        return new_name + ext

    counter = 1
    while True:
        filepath = os.path.join(for_path, new_name + ext)
        if not os.path.exists(filepath): break
        new_name = f"{date_name}_{counter}"
        counter += 1

    return filepath


def rename_files_using_dates(folder_path: str, extensions: list[str], recursive: bool):
    try:
        items = os.listdir(folder_path)
    except PermissionError:
        print_error(f"Нет доступа к папке: {folder_path}")
        return

    for item in items:
        # Не обрабатываем скрытые файлы и папки (macOS)
        if item.startswith('.'): continue

        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path) and recursive == True:
            rename_files_using_dates(item_path, extensions, recursive)

        elif not os.path.isfile(item_path):
            continue

        name, ext = os.path.splitext(item)
        if ext.strip('.').lower() not in extensions:
            continue

        creation_date = get_creation_date(item_path)
        new_name = filename_from_date(creation_date)
        if new_name == name:
            continue

        new_filepath = filename_from_date(creation_date, folder_path, ext)
        os.rename(item_path, new_filepath)
        print(f"{folder_path} : {item} → {os.path.basename(new_filepath)}")


if __name__ == "__main__":
    print("Переименование файлов по дате создания")
    folder = input("Введите путь к папке (или нажмите Enter для текущей): ").strip()
    if not folder: folder = "."

    if os.path.exists(folder) == False or os.path.isdir(folder) == False:
        print_error("Ошибка: указанный путь не существует или не является папкой.")
        exit(1)

    print(text_green("Будем переименовывать файлы по пути: "), Path(folder).expanduser().resolve())

    ext_text = input("Введите расширения файлов (через запятую): ").strip().lower()
    ext_list = [item for item in re.split(r'[.,\s]+', ext_text) if item and item != "py"]
    if len(ext_list) == 0:
        print_error("Не указаны валидные расширения файлов.")
        exit(1)

    print(text_green("Будем переименовывать файлы с расширениями: "), ext_list)

    include_sub = input("Обработать вложенные папки? (y/n): ").strip().lower() == "y"

    print(text_separator())
    rename_files_using_dates(folder, ext_list, include_sub)
    print_success("Все подходящие файлы переименованы.")
