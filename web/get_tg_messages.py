from time import sleep

from pyrogram import Client

from fastapi.requests import Request
from core.database import session, User
from core.settings import settings

__all__ = ["get_tg_messages"]

api_id = settings.TG_API_ID
api_hash = settings.TG_API_HASH
app = Client("/web/tg_account", api_id=api_id, api_hash=api_hash)


async def get_tg_messages(request: Request) -> list:

    if request.user.is_authenticated:  # get authenticated User
        user_id = request.user.identity
        with session() as s:
            user = s.query(User).filter_by(id=user_id.decode()).first()
        tg_groups = user.settings['tg_groups'].replace(" ", "").split(",")
        depth = int(user.settings['depth'])

    else:  # if no User authenticated
        tg_groups = ["myresume_ru", "juno_jobs", "pydevjob"]
        depth = 1

    tg_messages = []  # prepare messages list for template

    async with app:
        for group in tg_groups:
            async for message in app.get_chat_history(chat_id=group, limit=depth):

                # TODO apply filters (from separate module). chat.title + text
                # if pass then:
                tg_messages.append(message)

    return tg_messages
