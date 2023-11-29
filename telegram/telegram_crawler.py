# pip install pyrogram
# pip install tgcrypto

# import asyncio
from pyrogram import Client
from pyrogram.types import Message

from dotenv import load_dotenv
import os

load_dotenv()
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')

app = Client("my_account", api_id=api_id, api_hash=api_hash)

# async def main():  # Test messages to my personal tg account
#     async with app:
#         await app.send_message("me", "Hi again.")
#
#
# app.run(main())

# [my_test, @qa_jobs, @workayte, @it_jobs_agregator]
# chosen_groups = [-4035886753, -1001089317451, -1001091870362,-1001709625616]
# get group id: https://stackoverflow.com/a/69302407
# OR JUST filter by message.chat.username (tg chat handle):
chosen_groups = ["tele31415group", "qa_jobs", "workayte", "it_jobs_agregator"]


@app.on_message()  # https://docs.pyrogram.org/start/updates
async def my_handler(client, message: Message):  # pyrogram expects 2 parameters in handler
    # await message.forward("me")
    if message.chat.username in chosen_groups:
        # TODO save to db
        # save_to_db(group, time, message)
        # TODO message.text can be 'None' (when image sent, ...)
        print()
        print(f"***{message.chat.title}(@{message.chat.username}): {message.text}")  # full message example: temp.json
        print()
        print('-----------------------------------------------------------------')
    else:
        print(f"{message.chat.title}(@{message.chat.username}): {message.text}")
        print('-----------------------------------------------------------------')


app.run()
