from pyrogram.types import InlineKeyboardButton

class Data:

    generate_single_button = [InlineKeyboardButton("🔥 Start Generating Session 🔥", callback_data="generate")]

    home_buttons = [

        generate_single_button,

        [InlineKeyboardButton(text="🏠 Return Home 🏠", callback_data="home")]

    ]

    generate_button = [generate_single_button]
