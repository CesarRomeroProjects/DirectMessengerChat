# NAME: Cesar Damian Romero Amador
# EMAIL: cesardr1@uci.edu
# STUDENT ID: 31358030
import json
import time
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['response'])
DirectMessage = namedtuple('DirectMessage', ['response'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and
    convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(response)


def parse_direct_message(json_msg: str) -> DirectMessage:
    '''
    Parses a JSON string representing a Direct Message
    and returns a DirectMessage object.
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj
    except json.JSONDecodeError:
        print('JSON cannot be decoded.')

    return DirectMessage(response)


def send_direct_message(token, directmessage, username):
    '''
    Sends a direct message to the specified user using
    the provided token.
    '''
    return json.dumps(
        {"token": token,
         "directmessage": {"entry": directmessage,
                           "recipient": username,
                           "timestamp": f"{time.time()}"}})


def request_direct_messages(token, request):
    '''
    Returns a JSON string containing a request to send a
    direct message with the given token and message.
    '''
    return json.dumps(
        {"token": token, "directmessage": request})


def join_command(username, password):
    '''
    Encodes the join command in a JSON format and returns
    it as a string.
    '''
    return json.dumps(
        {"join": {"username": username,
                  "password": password,
                  "token": ""}})
