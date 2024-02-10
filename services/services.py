import os
import sys

BOOK_PATH = '/book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    # Если начальное значение плюс размер страницы больше всего текста
    # Возвращаем весь текст от начального значения и до конца
    if start + page_size > len(text):
        return text[start:start + page_size], len(text[start:start + page_size])

    # Обрезаем часть текста с запасом один символ
    text = text[start:start + page_size + 1]

    # Если обрезали текст в месте, где многоточие,
    # То убираем эти знаки
    if text[-1] in '.,:;!?' and text[-2] in '.,:;!?':
        while text[-1] in '.,:;!?':
            text = text[:-1]
    # Иначе убираем символ, который взяли с запасом
    else:
        text = text[:-1]

    # Дальше по тексту ищем любой знак препинания
    while text[-1] not in '.,:;!?':
        text = text[:-1]

    return text, len(text)


# Оформляем книгу в виде словаря
def prepare_book(path: str) -> None:
    # Считываем текст книги из файла
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()

    start_num = 0  # Позиция с которой начинается новая страница
    page_num = 0  # Номер страницы
    while True:
        # С помощью вспомогательной функции получаем текст и длину новой страницы
        text_page, delta_num = _get_part_text(text, start_num, PAGE_SIZE)

        start_num += delta_num
        page_num += 1

        # Добавляем новую страницу в словарь
        book[page_num] = text_page.lstrip()

        # Если позиция новой страницы равна длине текста книги выходим из цикла
        if start_num == len(text):
            break


prepare_book(os.path.join(sys.path[0] + os.path.normpath(BOOK_PATH)))

