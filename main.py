import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "" #paste ur token here

ADMIN_ID = #paste ur id here
bot = Bot(token=TOKEN)
dp = Dispatcher()

messages_data = {} 

@dp.message(Command("start"))
async def handle_start_command(message: Message):
    await message.reply("привет это подержка")
    
async def handle_user_message(message: Message):
    forwarded_message = await bot.forward_message(
        ADMIN_ID,
        message.chat.id,
        message.message_id
    )
    messages_data[forwarded_message.message_id] = message.from_user.id
    user_info = f"Сообщение от пользователя:\nID: {message.from_user.id}\nИмя: {message.from_user.first_name}\nНикнейм: @{message.from_user.username or '(нет никнейма)'}"
    await bot.send_message(ADMIN_ID, user_info)


async def handle_admin_reply(message: Message):
    if not message.reply_to_message: 
        await message.reply("Ответьте на пересланное сообщение, чтобы отправить его пользователю.")
        return

    replied_message_id = message.reply_to_message.message_id

    user_id = messages_data.get(replied_message_id)
    if not user_id:
        await message.reply("Не удалось найти пользователя для ответа.")
        return

    if message.text:
        await bot.send_message(user_id, f"{message.text}")
    elif message.photo:
        await bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption)
    elif message.video:
        await bot.send_video(user_id, video=message.video.file_id, caption=message.caption)
    elif message.document:
        await bot.send_document(user_id, document=message.document.file_id, caption=message.caption)
    elif message.voice:
        await bot.send_voice(user_id, voice=message.voice.file_id, caption=message.caption)
    elif message.video_note:
        await bot.send_video_note(user_id, video_note=message.video_note.file_id)
    elif message.audio:
        await bot.send_audio(user_id, audio=message.audio.file_id, caption=message.caption)
    elif message.sticker:
        await bot.send_sticker(user_id, sticker=message.sticker.file_id)
    else:
        await bot.send_message(user_id, "")

    await message.reply("Ответ переслан пользователю!")


dp.message.register(handle_user_message, lambda msg: msg.from_user.id != ADMIN_ID)
dp.message.register(handle_admin_reply, lambda msg: msg.from_user.id == ADMIN_ID)

async def main():
    print("bot is running0_0")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(main())
