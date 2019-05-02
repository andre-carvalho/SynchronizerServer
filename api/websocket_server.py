#!env/bin/python3
#from threading import Lock
from flask import Flask, render_template, request #session, 
from flask_socketio import SocketIO, emit, disconnect
import eventlet
import urllib.request
import urllib.parse
import jwt
import json

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
    points="""'[{"lat":21.22,"lng":2.33},{"lat":21.91,"lng":2.54},{"lat":21.76,"lng":2.11}]'"""
    return points


@socketio.on('newoccurrence', namespace='/occurrences')
def newOccurrence(message):
    # Message.occurrence template is: {}
    print('newoccurrence:', message)
    emit('occurrencebroadcast', {'occurrence': message}, broadcast=True)


@socketio.on('userposition', namespace='/occurrences')
def userPosition(message):
    # session['receive_count'] = session.get('receive_count', 0) + 1

    # Compute if any points intercepts the buffer region around message.point.
    # This point is the center of map for conected client.
    # Message.point template is: {point: {lat:23.33,lng:-3.55}}
    points = getNearPoints(message['point'])
    emit('nearpoints', {'points': points})


@socketio.on('pointsbroadcast', namespace='/occurrences')
def pointsBroadcast(message):
    # session['receive_count'] = session.get('receive_count', 0) + 1

    # Tell to all clients that one new point was added.
    if message['data']=='new_point':
        points = message['points']
        emit('nearpoints', {'points': points}, broadcast=True)

@socketio.on('connect', namespace='/occurrences')
def clientConnect():
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)
    #if token['data']!='':
    token = request.args.get('token')
    if isAuthorized(token):
        emit('connected', {'data': 'connected'})
    else:
        disconnect()

@socketio.on('disconnect', namespace='/occurrences')
def clientDisconnect():
    disconnect()
    print('Client disconnected', request.sid)


def isAuthorized(token):
    # verify if token is valid
    user = isValid(token)
    print(user)
    if user:
        headers = {"Authorization": "Bearer "+token}
        url = "http://127.0.0.1:5000/isAuthorized"

        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        print(response.getcode())
        data = response.read().decode('UTF-8')
        jsonObj = json.loads(data)
        if response.getcode()==200:
            if jsonObj['status']=='success' and jsonObj['data']['user_id']==user:
                return True
            else:
                return False
        else:
            print('invalid authorization')
            return False

def isValid(token):
    """
    Validates the auth token
    :param token:
    :return: integer to a valid payload sub or boolean if error message
    """
    SECRET_KEY='teste123'
    try:
        payload = jwt.decode(token, SECRET_KEY)
        # sub is user id
        return payload['sub']
        #return True
    except jwt.ExpiredSignatureError:
        #return 'Signature expired. Please log in again.'
        return False
    except jwt.InvalidTokenError:
        #return 'Invalid token. Please log in again.'
        return False

# @socketio.on('ping', namespace='/occurrences')
# def ping_pong():
#     emit('pong')

if __name__ == '__main__':
    socketio.run(ws, debug=True)