import os
import yt_dlp
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile

TOKEN = "7555414245:AAFAQ6FTcbyMuCGvm9IYCY4afxFyC4zJsbk"  # BotFather'dan tokenni kiriting
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Videoni yuklab olish funksiyasi
def download_instagram_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'instagram_video.mp4',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'instagram_video.mp4'

# /start komandasi
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Salom! Instagramdan video yuklash uchun menga link yuboring.")

# Instagram linkni qabul qilish
@dp.message(F.text)
async def download_video(message: Message):
    url = message.text.strip()
    
    if "instagram.com" not in url:
        await message.answer("Iltimos, to‘g‘ri Instagram video linkini yuboring!")
        return

    await message.answer("Videoni yuklab olyapman, kuting...")

    try:
        video_path = download_instagram_video(url)

        # ✅ FSInputFile orqali videoni to‘g‘ri formatda yuboramiz
        video_file = FSInputFile(video_path)

        await message.answer_video(video_file)

        os.remove(video_path)  # Yuklab olingan faylni o‘chiramiz
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")

# Botni ishga tushirish
async def main():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Botni ishga tushirish"),
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
