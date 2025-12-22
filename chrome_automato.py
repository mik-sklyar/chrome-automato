import os
import threading
from pathlib import Path

import nodriver as nr

from unify_downloads import unify_downloads
from workers import *

_needs_pause = True
_needs_exit = False


async def main(user_path: str, scheme: Scheme):
    print(text_separator('='))
    print_success(f"Запуск браузера для пользователя [{user_path}] и схемы работы [{scheme.name}]")
    print(text_separator('='))

    profile_path = os.path.join(Path(__file__).parent.absolute(), Config.users_path.value, user_path)
    browser = await nr.start(headless=False, user_data_dir=profile_path)
    print("Ждём пока загрузится браузер и раздуплится Adblock...")
    await browser.wait(10)
    page = await browser.get(scheme.url)

    work_func = [save_image_and_refresh, save_two_images_and_refresh][scheme.id]

    is_paused = False
    seconds_count = 0

    while not _needs_exit:
        if _needs_pause:
            if not is_paused:
                print("Настрой что надо и нажми Enter для начала работы...")
                is_paused = True
            await page.sleep(1)
            continue
        else:
            if is_paused:
                print(text_separator())
                print_success("Работаем :)")
                seconds_count = scheme.waiting_period
                is_paused = False

        await page.sleep(1)
        seconds_count += 1
        if seconds_count < scheme.waiting_period:
            print(".", end="", flush=True)
            continue

        print("")
        await work_func(page, scheme)
        seconds_count = 0


def start_main_with_event_loop(user_path: str, scheme: Scheme):
    nr.loop().run_until_complete(main(user_path, scheme))


if __name__ == '__main__':
    unify_downloads()

    print_success("Добро пожаловать в Chrome-Automato! Давай-ка накачаем не скучных картинок (*‿*)")
    users = Config.users.value
    users_str = ", ".join(map(lambda i_u: f"[{i_u[0] + 1}][{text_green(i_u[1])}]", enumerate(users)))
    choice = input(f"Выберите пользователя {users_str}:").strip()
    user_index: int = 0
    try:
        user_index = int(choice) - 1
        if user_index < 0 or user_index > len(users): raise ValueError
    except Exception as e:
        if isinstance(e, KeyboardInterrupt): raise
        user_index = 0

    schemes = Config.schemes.value
    schemes_str = ", ".join(map(lambda i_u: f"[{i_u[0] + 1}][{text_green(i_u[1].name)}]", enumerate(schemes)))
    choice = input(f"Выберите схему работы {schemes_str}: ").strip()
    scheme_index = 1
    try:
        scheme_index = int(choice) - 1
        if scheme_index < 0 or scheme_index > len(schemes): raise ValueError
    except Exception as e:
        if isinstance(e, KeyboardInterrupt): raise
        scheme_index = 0

    threading.Thread(target=start_main_with_event_loop, args=(users[user_index], schemes[scheme_index]),
                     daemon=True).start()
    while True:
        choice = input()
        if choice.strip().lower() == "q":
            _needs_exit = True; break
        else:
            _needs_pause = not _needs_pause
