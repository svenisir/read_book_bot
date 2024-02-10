from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def echo_send(message: Message):
    await message.send_copy(chat_id=message.chat.id)
