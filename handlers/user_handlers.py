from copy import deepcopy

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from models.models import user_data, users
from filters.filters import IsDelBookmarksCallbackData, IsDigitCallbackData
from services.services import book
from keyboards.bookmarks_kb import create_bookmarks_kb, edit_bookmarks_kb
from keyboards.pagination_kb import generate_pagination_kb
from lexicon.lexicon import LEXICON

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])
    if message.from_user.id not in users:
        users[message.from_user.id] = deepcopy(user_data)


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands=['beginning']))
async def process_beginning_command(message: Message):
    users[message.from_user.id]['page'] = 1
    text = book.get(users.get(message.from_user.id, {}).get('page', 0),
                    'Введите команду старт для регистрации!')
    await message.answer(
        text=text,
        reply_markup=generate_pagination_kb(
            'backward',
            f'{users.get(message.from_user.id, {}).get("page", 0)}/{len(book)}',
            'forward'
        )
    )


@router.message(Command(commands=['continue']))
async def process_continue_command(message: Message):
    await message.answer(
        text=book.get(users.get(message.from_user.id, {}).get('page', 0),
                      'Введите команду старт для регистрации!'),
        reply_markup=generate_pagination_kb(
            'backward',
            f'{users.get(message.from_user.id, {}).get("page", 0)}/{len(book)}',
            'forward'
        )
    )


@router.message(Command(commands=['bookmarks']))
async def process_bookmarks_command(message: Message):
    if users[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_kb(
                *users[message.from_user.id]['bookmarks']
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'backward')
async def process_backward_command(callback: CallbackQuery):
    if users[callback.from_user.id]['page'] > 1:
        users[callback.from_user.id]['page'] -= 1
        text = book[users[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=generate_pagination_kb(
                'backward',
                f'{users[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'forward')
async def process_forward_command(callback: CallbackQuery):
    if users[callback.from_user.id]['page'] <= len(book):
        users[callback.from_user.id]['page'] += 1
        text = book[users[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=generate_pagination_kb(
                'backward',
                f'{users[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def add_bookmarks(callback: CallbackQuery):
    users[callback.from_user.id]['bookmarks'].add(
        users[callback.from_user.id]['page']
    )
    await callback.answer(
        text='Страница добавлена в закладки!',
        show_alert=True
    )


@router.callback_query(IsDigitCallbackData())
async def go_to_page(callback: CallbackQuery):
    text = book[int(callback.data)]
    users[callback.from_user.id]["page"] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=generate_pagination_kb(
            'backward',
            f'{users[callback.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )


@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


@router.callback_query(F.data == 'edit_bookmarks_button')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks_button'],
        reply_markup=edit_bookmarks_kb(
            *users.get(callback.from_user.id, 0).get('bookmarks', 0)
        )
    )


@router.callback_query(IsDelBookmarksCallbackData())
async def process_del_press(callback: CallbackQuery):
    users[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    if users[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=edit_bookmarks_kb(
                *users.get(callback.from_user.id, 0).get('bookmarks', 0)
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
