#!env/bin/python3
#from threading import Lock
from flask import Flask, render_template, request #session, 
from flask_socketio import SocketIO, emit, disconnect
import eventlet

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = 'eventlet'

ws = Flask(__name__)
ws.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(ws, async_mode=async_mode)
# thread = None
# thread_lock = Lock()


# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('server_response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/occurrences')

def getNearPoints(point):
    print('Receive new point(client center map)', point)
    points="""[{lat:21.22,long:2.33},{lat:21.91,long:2.54},{lat:21.76,long:2.11}]"""
    return points



@ws.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('client_request', namespace='/occurrences')
def test_message(message):
    # session['receive_count'] = session.get('receive_count', 0) + 1

    # Compute if any points intercepts the buffer region around message.point.
    # This point is the center of map for conected client.
    # Message.point template is: {point: {lat:23.33,long:-3.55}}
    points = getNearPoints(message['point'])
    emit('server_response',
         {'data': 'new_point_confirmed', 'points': points})


@socketio.on('broadcast_event', namespace='/occurrences')
def test_broadcast_message(message):
    # session['receive_count'] = session.get('receive_count', 0) + 1

    # Tell to all clients that one new point was added.
    if message['data']=='new_point':
        emit('server_response',
            {'data': 'new_point_confirmed', 'points': '[]'},
            broadcast=True)
    


@socketio.on('disconnect_request', namespace='/occurrences')
def disconnect_request():
    # session['receive_count'] = session.get('receive_count', 0) + 1
    # emit('server_response',
    #      {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/occurrences')
def test_connect():
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)
    emit('server_response', {'data': 'connected', 'points': '[]'})


@socketio.on('disconnect', namespace='/occurrences')
def test_disconnect():
    print('Client disconnected', request.sid)


# @socketio.on('ping', namespace='/occurrences')
# def ping_pong():
#     emit('pong')

if __name__ == '__main__':
    socketio.run(ws, debug=True)