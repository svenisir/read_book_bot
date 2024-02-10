from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.services import book


def create_bookmarks_kb(*args: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[InlineKeyboardButton(
        text=f'Страница {num}. {book[num][:100]}...',
        callback_data=str(num),
    ) for num in sorted(args)], width=1)

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_bookmarks_button'],
            callback_data='edit_bookmarks_button'
        ),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        ),
        width=2
    )

    return kb_builder.as_markup()


def edit_bookmarks_kb(*args: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[InlineKeyboardButton(
        text=f'{LEXICON["del"]} Страницу {num}. {book[num][:100]}...',
        callback_data=f'{num}del',
    ) for num in sorted(args)], width=1)

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        )
    )

    return kb_builder.as_markup()
