import asyncio

from apps.users.consumers import sio


def send_sms(event, data, room):
    asyncio.run(sio.emit(event=event, data=data, room=room))
