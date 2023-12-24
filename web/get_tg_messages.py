from pyrogram import Client

from fastapi.requests import Request
from core.database import session, User
from core.settings import tg_client

from .filter_tg_message import filter_tg_message

__all__ = ["get_tg_messages"]


async def get_tg_messages(request: Request) -> list:

    if request.user.is_authenticated:  # get authenticated User
        user_id = request.user.identity
        with session() as s:
            user = s.query(User).filter_by(id=user_id.decode()).first()

        tg_groups = user.settings['tg_groups'].replace(" ", "").split(",")
        filter_in = user.settings['filter_in'].replace(" ", "").split(",")
        filter_out = user.settings['filter_out'].replace(" ", "").split(",")
        depth = user.settings['depth']

    else:  # if no authenticated User (example)
        tg_groups = ["myresume_ru", "juno_jobs", "pydevjob"]  # TODO if tg group change chat.title, better to use IDs
        depth = 1

    tg_messages = []  # prepare messages list for template

    async with tg_client:
        for group in tg_groups:

            async for message in tg_client.get_chat_history(chat_id=group, limit=depth):

                if request.user.is_authenticated:
                    # Applying filter from User's settings
                    if await filter_tg_message(filter_in=filter_in, filter_out=filter_out, message=message):
                        tg_messages.append(message)
                    else:
                        continue
                else:  # if no authenticated User (example)
                    tg_messages.append(message)

    return tg_messages
