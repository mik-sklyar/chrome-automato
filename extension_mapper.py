import re


class ExtensionMapper:
    def __init__(self, extensions_str=""):
        self.__map_all_unknown = False
        self.__extension_map = {}
        self.parse_extensions(extensions_str)

    def parse_extensions(self, extensions_str):
        if not extensions_str.strip(): return

        if "*" in extensions_str:
            self.__map_all_unknown = True

        items = re.split(r'\s*[.,*]\s*', extensions_str.strip())
        for item in items:
            extensions = item.split(':')
            mapped = extensions[len(extensions) - 1].strip(" .")
            if not _is_valid_extension(mapped): continue
            for ext in extensions:
                original = ext.strip(" .")
                if not _is_valid_extension(original): continue
                self.__extension_map[original] = mapped

    def has_mapping(self, extension) -> bool:
        if not _is_valid_extension(extension.lower()): return False

        if self.__map_all_unknown: return True

        return ext in self.__extension_map

    def get_mapped_extension(self, extension):
        ext = extension.lower()
        if not _is_valid_extension(ext): return None

        mapped = self.__extension_map.get(ext)
        if mapped is None and self.__map_all_unknown:
            mapped = ext

        return mapped


def _is_valid_extension(ext: str) -> bool:
    if not ext: return False

    # Запрещённые символы в именах файлов (для кросс-платформенности)
    forbidden_chars = set(r'<>:"/\|?* ')
    if any(char in forbidden_chars for char in ext):
        return False

    # Дополнительно: разрешены только буквы, цифры, - и _
    if not re.fullmatch(r'[a-zA-Z0-9._-]+', ext):
        return False

    # Проверка на системные имена (Windows)
    windows_reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                        'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    if ext.upper() in windows_reserved:
        return False

    # Расширение не должно быть слишком длинным (обычно до 10–12 символов)
    if len(ext) > 12:
        return False

    return True


# Пример использования:
if __name__ == "__main__":

    print("Введите расширения файлов для замены разделённые двоеточием."
          " Группы расширений разделяются запятой."
          " Если будет *, то для любого расширения \"найдётся\" соответствие:")
    mapper = ExtensionMapper(input().strip().lower())

    while True:
        ext_to_check = mapper.get_mapped_extension(input("Проверим соответствие расширения:"))
        if ext_to_check is None:
            print("нет соответствия")
            continue
        print(f"соответствие: {ext_to_check}")
