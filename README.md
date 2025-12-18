# chrome-automato

Проект для автоматизации работы браузера Google Chrome с использованием библиотеки NoDriver на примере сохранения изображений с сайта с необходимостью совершать дополнительные рутинные действия и ожидать получения результата.

## Нужно для работы:

* Python 3.10\+
* [NODRIVER](https://github.com/ultrafunkamsterdam/nodriver)
* Google Chrome (проверено на версии 143, macOS)
* Упорство, труд и высокая цель

## Описание:

* chrome-automato.py - основной скрипт, запускает браузер и делает красиво
* config.py - необходимые констаны для работы
* workers.py - набор функций для разных режимов работы (что собственно делать на целевом сайте)
* rename_by_date.py - самостоятельный скрипт для переименования файлов в папке используя в качестве имени дату создания, под капотом задействует extension_mapper.py, если ещё нужно привести расширения файлов к единому стилю
* download_image.py - самостоятельный скрипт для простого скачивания картинки по url в заданную папку

## Ссылки:

* [NODRIVER Documentation](https://ultrafunkamsterdam.github.io/nodriver/nodriver/quickstart.html)
* [XPath — быстрый гайд](https://testengineer.ru/xpath-quick-guide/)
* [Шпаргалка по XPath и CSS-селекторам](https://habr.com/ru/articles/817555/)
