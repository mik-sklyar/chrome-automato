from config import *
from download_image import download_image
from print_utils import *


async def _get_refresh_button(page, scheme: Scheme):
    try:
        elements = await page.xpath(scheme.edit_xpath)
        if len(elements) == 0:
            raise Exception()
        textedit = elements[0]
    except Exception as e:
        if isinstance(e, KeyboardInterrupt): raise
        return None

    await textedit.click()
    await page.sleep(1)

    try:
        elements = await page.xpath(scheme.refresh_xpath)
        if len(elements) == 0:
            raise Exception()
        button = elements[0]
    except Exception as e:
        if isinstance(e, KeyboardInterrupt): raise
        return None

    return button

async def save_image_and_refresh(page, scheme: Scheme):
    button = await _get_refresh_button(page, scheme)
    if button is None:
        return

    try:
        elements = await page.xpath(scheme.image_xpath)
        src_value = elements[0].attrs["src"]
        await download_image(src_value, scheme.download_path)
        await button.click()
        print_success("Скачал и нажал на обновление")
    except Exception as e:
        print_error(f"Ошибка поиска картинки: {e}")

async def save_two_images_and_refresh(page, scheme: Scheme):
    button = await _get_refresh_button(page, scheme)
    if button is None:
        return

    try:
        elements = await page.xpath(scheme.image_xpath)
        src_value1: str = elements[0].attrs["src"]
        src_value2 = src_value1.rstrip("1") + "2"
        await download_image(src_value1, scheme.download_path)
        await download_image(src_value2, scheme.download_path)
        await button.click()
        print_success("Скачал и нажал на обновление")
    except Exception as e:
        print_error(f"Ошибка поиска картинки: {e}")
