import asyncio
import sys
from datetime import datetime
from pathlib import Path

import aiohttp

from print_utils import *
from rename_by_date import filename_from_date


async def download_image(url: str, path_to_save: str = ""):
    try:
        images_dir = Path(path_to_save).expanduser().resolve()

        images_dir.mkdir(exist_ok=True)

        file_path = Path(filename_from_date(datetime.now(), path_to_save, ".jpg")).expanduser().resolve()

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    return str(file_path)
                else:
                    raise Exception(f"статус запроса {response.status}")
    except Exception as e:
        print_error(f"Ошибка сохранения картинки: {e}")
        return None


async def main(url: str, path: str = ""):
    await download_image(url, path)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Этот скрипт принимает на вход аргументы:")
        print("первый - url картинки (обязательный)")
        print("второй - путь для сохранения картинки")
        exit(1)

    image_url = sys.argv[1]
    image_path = sys.argv[2] if len(sys.argv) > 2 else ""
    asyncio.run(main(image_url, image_path))
