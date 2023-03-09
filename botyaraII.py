import urllib
from urllib import request
from PIL import Image, ImageDraw, ImageFont
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot
from pillow_heif import register_heif_opener
import datetime
import os
bot = Bot('BOT_TOKEN')
dp = Dispatcher(bot)
symbols = [i for i in '@$0B#NGWM8RDHPOKZ96khEPXS2wmeyjufF]}{tx1zv7lciL/\\|?*>r^;:_\"~,\'-.`']
font2 = ImageFont.truetype("arial.ttf", 5, encoding="unic")

register_heif_opener()


async def edit_message(message: types.Message, text):
    new_mess = await message.edit_text(text, parse_mode='Markdown')
    return new_mess


def delete_file(file):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)
    os.remove(path)


async def photo_in_symbols(file, tile, chat_id, new_file_name):
    photo = file
    img = Image.open(photo)
    symb_image = Image.new('RGB', (img.size[0], img.size[1]), 'white')
    width = img.size[0] // tile
    height = img.size[1] // tile
    img = img.resize((width, height))
    draw = ImageDraw.Draw(symb_image)
    goal = width * height
    pix = img.load()
    process = 0
    prcs = 999
    k = 0
    message = await bot.send_message(chat_id, 'обработано 0% \n □□□□□□□□□□')
    for x in range(width):
        for y in range(height):
            draw.text((x * tile, y * tile),
                      symbols[(pix[x, y][0] + pix[x, y][1] + pix[x, y][2]) // 12],
                      font=font2, fill="#000000")
            process += 1
            if prcs != round(process / goal * 100, 2):
                if round(process / goal * 100, 2) % 5 == 0 and process != 1:
                    k += 0.5
                    progressbar = '■' * int(k) + '□' * (10 - int(k))
                    await edit_message(message, f'обработано {round(process / goal * 100, 2)}% \n'
                                                f'[{progressbar}]')
                prcs = round(process / goal * 100, 2)
    symb_image.save(new_file_name)
    delete_file(file)


@dp.message_handler(content_types=['document'])
async def scan_message(msg: types.Message):
    document_id = msg.document.file_id
    file_info = await bot.get_file(document_id)
    fi = file_info.file_path
    name = msg.document.file_name
    new_file_name = f'{datetime.datetime.now().time().microsecond}.jpg'
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot5733192318:AAGJAH6rAfxPaVvgeL2bjMmLmiY-_SSiR54/{fi}', f'./{name}')
    await msg.answer('секунду..')
    if name.split('.')[-1].lower in ('mp4', 'mov'):
        await msg.answer('я пока не умею работать с видео')
    else:
        await photo_in_symbols(name, 5, msg.chat.id, new_file_name)
    file = open(new_file_name, 'rb')
    await bot.send_document(msg.chat.id, (new_file_name, file))
    delete_file(new_file_name)

if __name__ == '__main__':
    executor.start_polling(dp)
