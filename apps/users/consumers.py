import socketio

# Создаем экземпляр Socket.IO сервера

sio = socketio.AsyncServer(async_mode='asgi')

UZB_ROOM = "uzbek_sms_room"


@sio.event
async def connect(sid, environ):
    await sio.enter_room(sid, UZB_ROOM)
    print('Client connected:', sid)


@sio.event
async def disconnect(sid):
    print('Client disconnected:', sid)


@sio.event
async def message(sid, data):
    print('Message from', sid, ':', data)
    await sio.emit('notification', {'data': 'Message received!'}, room=UZB_ROOM)
