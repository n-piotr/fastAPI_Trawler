"""
from https://docs.pyrogram.org/intro/quickstart:

- Install Pyrogram with pip3 install -U pyrogram.
- Obtain the API_ID and API_HASH by following Telegram’s instructions and rules at https://core.telegram.org/api/obtaining_api_id
- Save TG_API_ID = '***' and TG_API_HASH = '***' in .env file
- Run this script
- Follow the instructions on your terminal to login.
- Watch Pyrogram send a message to yourself and generate tg_account.session file
- Add *.session and .env to .gitignore
"""

import asyncio
from pyrogram import Client

from dotenv import load_dotenv
import os

load_dotenv()
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')


async def main():
    async with Client("tg_account", api_id, api_hash) as app:
        await app.send_message("self", ">> tg_account.session file generated <<")


asyncio.run(main())
