import os
from datetime import datetime
from pathlib import Path

from extension_mapper import ExtensionMapper
from print_utils import *

filename_date_format = "%Y-%m-%d_%H-%M-%S"
_verbose = False

def get_creation_date(filepath):
    try:
        stat = os.stat(filepath)

        import platform
        if platform.system() == 'Darwin':  # macOS
            return datetime.fromtimestamp(stat.st_birthtime)

        # Linux, Windows
        return datetime.fromtimestamp(stat.st_ctime)
    except Exception as e:
        if _verbose: print(f"Ошибка при получении даты создания: {e}")
        return None


def filename_from_date(date: datetime, for_path: str = "", ext: str = "") -> str:
    ext = ext.strip(".")
    if len(ext) > 0:
        ext = "." + ext

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


def rename_files_using_dates(folder_path: str, extensions_str: str, recursive: bool):
    try:
        items = os.listdir(folder_path)
    except PermissionError:
        if _verbose: print_error(f"Нет доступа к папке: {folder_path}")
        return

    mapper = ExtensionMapper(extensions_str)

    for item in items:
        # Не обрабатываем скрытые файлы и папки (macOS)
        if item.startswith('.'): continue

        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path) and recursive == True:
            rename_files_using_dates(item_path, extensions_str, recursive)

        elif not os.path.isfile(item_path):
            continue

        name, ext = os.path.splitext(item)
        ext = mapper.get_mapped_extension(ext.strip('.').lower())
        if ext is None:
            continue

        creation_date = get_creation_date(item_path)
        new_name = filename_from_date(creation_date, ext=ext)
        if new_name == item:
            continue

        new_filepath = filename_from_date(creation_date, folder_path, ext)
        os.rename(item_path, new_filepath)
        if _verbose: print(f"{folder_path} : {item} → {os.path.basename(new_filepath)}")


if __name__ == "__main__":
    _verbose = True
    print("Переименование файлов по дате создания")
    folder = input("Введите путь к папке (или нажмите Enter для текущей): ").strip()
    if not folder: folder = "."

    if os.path.exists(folder) == False or os.path.isdir(folder) == False:
        print_error("Ошибка: указанный путь не существует или не является папкой.")
        exit(1)

    print(text_green("Будем переименовывать файлы по пути: "), Path(folder).expanduser().resolve())

    ext_text = input("Введите расширения файлов (через запятую): ").strip().lower()

    include_sub = input("Обработать вложенные папки? (y/n): ").strip().lower() == "y"

    print(text_separator())
    rename_files_using_dates(folder, ext_text, include_sub)
    print_success("Все подходящие файлы переименованы.")
