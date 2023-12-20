__all__ = ["filter_tg_message"]


async def filter_tg_message(filter_in, filter_out, message):  # TODO types

    # print(message.text[:20], filter_in, filter_out)

    # Filter IN
    for key in filter_in:
        try:
            if key.lower() not in (message.chat.title + message.text).lower():
                print(f"> {message.chat.title} / {message.text[:20]}... FILTERED OUT")
                return False
        except TypeError as e:  # TODO processing messages with images
            print(f"> Caught an error: {e}. (https://t.me/{message.chat.username}/{message.id})")
            return False

    # Filter OUT
    # ... TODO

    return True
