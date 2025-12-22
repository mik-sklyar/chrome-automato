from enum import Enum

class Scheme:
    __obj_count = 0

    def __init__(self, name, url, edit_xpath, image_xpath, refresh_xpath, download_path, waiting_period):
        self.id = Scheme.__obj_count; Scheme.__obj_count += 1
        self.name = name
        self.url = url
        self.edit_xpath = edit_xpath
        self.image_xpath = image_xpath
        self.refresh_xpath = refresh_xpath
        self.download_path = download_path
        self.waiting_period = waiting_period

class Config(Enum):
    schemes = [
        Scheme('Обычная',
               'some usual url',
               '',
               'some usual image xpath',
               'some usual button xpath',
               'Downloads',
               15),
        Scheme('Особенная',
               'another url',
               'some xpath for textarea',
               'another image xpath',
               'another button xpath"]',
               'Downloads',
               15),
    ]
    users_path = 'ChromeAccounts'
    users = ["user1", "user2", "user3"]
