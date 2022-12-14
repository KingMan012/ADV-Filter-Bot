#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


import re
import pyrogram

from pyrogram import (
    filters,
    Client
)

from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Message,
    CallbackQuery,
)

from bot import Bot
from script import script
from database.mdb import searchquery
from plugins.channel import deleteallfilters
from config import AUTH_USERS

BUTTONS = {}

@Client.on_message(filters.group & filters.text)
async def filter(client: Bot, message: Message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if 2 < len(message.text) < 100:    
        btn = []

        group_id = message.chat.id
        name = message.text

        filenames, links = await searchquery(group_id, name)
        if filenames and links:
            for filename, link in zip(filenames, links):
                btn.append(
                    [InlineKeyboardButton(text=f"๐ฅ {filename}",url=f"{link}")]
            )
           
        else:
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"๐ฅ {message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="๐ Pages 1/1 ๐",callback_data="pages")]
            )
            buttons.append(
                [InlineKeyboardButton("๐ต MSR VIP Series Member แแแบแแแบ ๐ต", url="https://t.me/MSR_VIP_Bot")]
            )
            buttons.append(
                [InlineKeyboardButton("๐ LinkแแฝแฑแแฒแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธJoinแแซ ๐", url="https://t.me/msrlinkcollection/43")]
            )
            await message.reply_text(
                f"<b>Hi  {message.from_user.mention} ๐\n\n{message.from_user.mention} แแพแฌแแฑแแฒแทแแฏแแบแแพแแบ ๐๐ป {message.text}๐๐ป  แแญแฏ แแปแแฑแฌแบ Bot แแแพแฌแแฑแธแแฌแธแแแบแแฑแฌแบแ ๐\n\n<b>๐๐ปโโ๏ธ แแฑแฌแแบแธแแญแฏแแฐ  : {message.from_user.mention}</b>\n\n<b>๐ Join Our Main Channel Link \n๐บ MSR Movie Link Collection  ๐๐ป @MSRLINKCOLLECTION ๐๐ป \n๐ต MSR VIP Channel  ๐๐ป @SERIESLIST_VIP ๐๐ป</b>\n</b>๐ง๐ปโ๐ป Uploaded By  : MSR Channel Team</a>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT PAGE โฉ",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"๐ Pages 1/{data['total']} ๐",callback_data="pages")]
        )
        buttons.append(
            [InlineKeyboardButton("๐ต MSR VIP Series Member แแแบแแแบ ๐ต", url="https://t.me/MSR_VIP_Bot")]
        )
        buttons.append(
            [InlineKeyboardButton("๐ LinkแแฝแฑแแฒแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธJoinแแซ ๐", url="https://t.me/msrlinkcollection/43")]
        )

        await message.reply_text(
                f"<b>Hi  {message.from_user.mention} ๐\n\n{message.from_user.mention} แแพแฌแแฑแแฒแทแแฏแแบแแพแแบ ๐๐ป {message.text}๐๐ป  แแญแฏ แแปแแฑแฌแบ Bot แแแพแฌแแฑแธแแฌแธแแแบแแฑแฌแบแ ๐\n\n<b>๐๐ปโโ๏ธ แแฑแฌแแบแธแแญแฏแแฐ  : {message.from_user.mention}</b>\n\n<b>๐ Join Our Main Channel Link \n๐บ MSR Movie Link Collection  ๐๐ป @MSRLINKCOLLECTION ๐๐ป \n๐ต MSR VIP Channel  ๐๐ป @SERIESLIST_VIP ๐๐ป</b>\n</b>๐ง๐ปโ๐ป Uploaded By  : MSR Channel Team</a>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )    


@Client.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    clicked = query.from_user.id
    typed = query.message.reply_to_message.from_user.id

    if (clicked == typed) or (clicked in AUTH_USERS):

        if query.data.startswith("next"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("แแแบแแแบ แแปแฝแแบแฏแแบแ แแแบแแฑแทแแปแบแแฑแฌแแบแธแแปแฌแธแแฒแแพ แแแบแแฏแกแแฝแแบ แแแบแธแแญแฏ แกแแฏแถแธแแผแฏแแฑแแแบแ แแปแฑแธแแฐแธแแผแฏแ แแฑแฌแแบแธแแญแฏแแปแแบแแญแฏ แแแบแแถแแฑแธแแญแฏแทแแซแ",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("โช BACK PAGE", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"๐ Pages {int(index)+2}/{data['total']} ๐", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐ต MSR VIP Series Member แแแบแแแบ ๐ต", url="https://t.me/MSR_VIP_Bot")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐ LinkแแฝแฑแแฒแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธJoinแแซ ๐", url="https://t.me/msrlinkcollection/43")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("โช BACK PAGE", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT โฉ", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"๐ Pages {int(index)+2}/{data['total']} ๐", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐ต MSR VIP Series Member แแแบแแแบ ๐ต", url="https://t.me/MSR_VIP_Bot")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐ LinkแแฝแฑแแฒแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธJoinแแซ ๐", url="https://t.me/msrlinkcollection/43")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("แแแบแแแบ แแปแฝแแบแฏแแบแ แแแบแแฑแทแแปแบแแฑแฌแแบแธแแปแฌแธแแฒแแพ แแแบแแฏแกแแฝแแบ แแแบแธแแญแฏ แกแแฏแถแธแแผแฏแแฑแแแบแ แแปแฑแธแแฐแธแแผแฏแ แแฑแฌแแบแธแแญแฏแแปแแบแแญแฏ แแแบแแถแแฑแธแแญแฏแทแแซแ.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT PAGE โฉ", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"๐ Pages {int(index)}/{data['total']} ๐", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐ต MSR VIP Series Member แแแบแแแบ ๐ต", url="https://t.me/MSR_VIP_Bot")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐ LinkแแฝแฑแแฒแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธJoinแแซ ๐", url="https://t.me/msrlinkcollection/43")]
                )
  
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("โช BACK PAGE", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT โฉ", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"๐ Pages {int(index)}/{data['total']} ๐", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐ต MSR VIP Series Member แแแบแแแบ ๐ต", url="https://t.me/MSR_VIP_Bot")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐ LinkแแฝแฑแแฒแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธJoinแแซ ๐", url="https://t.me/msrlinkcollection/43")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data == "pages":
            await query.answer()


        elif query.data == "start_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("HELP", callback_data="help_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data")],
                [InlineKeyboardButton("๐ JOIN OUR MAIN CHANNEL ๐ ", url="https://t.me/msrlinkcollection")]
            ])

            await query.message.edit_text(
                script.START_MSG.format(query.from_user.mention),
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "help_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="start_data"),
                    InlineKeyboardButton("ABOUT ", callback_data="about_data")],
                [InlineKeyboardButton("๐ง SUPPORT ๐ง", url="https://t.me/+i75L1OqRZnRlZDY9")]
            ])

            await query.message.edit_text(
                script.HELP_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "about_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="help_data"),
                    InlineKeyboardButton("START", callback_data="start_data")],
                [InlineKeyboardButton(" ๐งพ SOURCE CODE ๐งพ", url="https://t.me/msr_kabar")]
            ])

            await query.message.edit_text(
                script.ABOUT_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "delallconfirm":
            await query.message.delete()
            await deleteallfilters(client, query.message)
        
        elif query.data == "delallcancel":
            await query.message.reply_to_message.delete()
            await query.message.delete()

    else:
        await query.answer("แแญแแบแแฝแฑ แแฐแแปแฌแธแแญแฏแแบแแฌแธแแฌแแผแฎแธแแฑ\n\n๐  แแพแญแแบแแปแแบแแแบ Groupแแฒ แแญแฏแแบแทแแฌแแญแฏแแบแแญแฏแแญแฏแแบแแพแฌแแซ ๐ฅณ\n\n๐ง๐ปโ๐ป Uploaded By :Kabar Kyaw ",show_alert=True)


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]  
