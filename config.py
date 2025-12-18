from enum import Enum

class Scheme:
    def __init__(self, name, url, edit_xpath, image_xpath, refresh_xpath, identifier):
        self.name = name
        self.url = url
        self.edit_xpath = edit_xpath
        self.image_xpath = image_xpath
        self.refresh_xpath = refresh_xpath
        self.identifier = identifier

class Config(Enum):
    users = ["user1", "user2", "user3"]
    schemes = [
        Scheme('Обычная',
               'some usual url',
               '',
               'some usual image xpath',
               'some usual button xpath',
               0),
        Scheme('Особенная',
               'another url',
               'some xpath for textarea',
               'another image xpath',
               'another button xpath"]',
               1)
    ]