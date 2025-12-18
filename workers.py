from config import *
from download_image import download_image
from print_utils import *


async def save_image_and_refresh(page, scheme: Scheme):
    try:
        elements = await page.xpath(scheme.refresh_xpath)
        if len(elements) == 0:
            raise Exception()
        button = elements[0]
    except:
        return

    try:
        elements = await page.xpath(scheme.image_xpath)
        src_value = elements[0].attrs["src"]
        await download_image(src_value, "Downloads")
        await button.click()
        print_success("Скачал и нажал на обновление")
    except Exception as e:
        print_error(f"Ошибка поиска картинки: {e}")


async def save_two_images_and_refresh(page, scheme: Scheme):
    try:
        elements = await page.xpath(scheme.edit_xpath)
        if len(elements) == 0:
            raise Exception()
        textedit = elements[0]
    except:
        return

    await textedit.click()
    await page.sleep(1)

    try:
        elements = await page.xpath(scheme.refresh_xpath)
        if len(elements) == 0:
            raise Exception()
        button = elements[0]
    except:
        return

    try:
        elements = await page.xpath(scheme.image_xpath)
        src_value1: str = elements[0].attrs["src"]
        src_value2 = src_value1.rstrip("1") + "2"
        await download_image(src_value1, "Downloads")
        await download_image(src_value2, "Downloads")
        await button.click()
        print_success("Скачал и нажал на обновление")
    except Exception as e:
        print_error(f"Ошибка поиска картинки: {e}")
