# NAME: Cesar Damian Romero Amador
# EMAIL: cesardr1@uci.edu
# STUDENT ID: 31358030
import socket
import json
import ds_protocol


def join_server(username: str, password: str):
    """
    Connects to the ICS 32 Distributed Social server and attempts to
    join with the specified username and password.

    Args:
        username (str): The username to use for the join attempt.
        password (str): The password to use for the join attempt.

    Returns:
        A tuple containing the authentication token,
        the send file object, and the receive file object.

    Raises:
        AssertionError: If the response from the server is not one of
                        the expected outputs.
        ConnectionError: If the client is unable to connect to the server.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        server = '168.235.86.101'
        port = 3021
        client.connect((server, port))
        send = client.makefile('w')
        recv = client.makefile('r')
        join_msg = ds_protocol.join_command(username, password)
        assert join_msg == '{"join": ' \
               f'{{"username": "{username}", ' \
               f'"password": "{password}", ' \
               '"token": ""}}'
        send.write(join_msg + '\r\n')
        send.flush()
        token = ""
        join_response = ds_protocol.extract_json(recv.readline()[:-1])
        join_response = join_response.response
        if join_response['response']['type'] == 'ok':
            token = join_response['response']['token']
        expected_outputs = [{
            'response': {'type': 'ok',
                         'message': 'Welcome to the ICS 32 ' +
                         'Distributed Social!',
                         'token': token}},
                           {
            'response': {'type': 'ok',
                         'message': f'Welcome back, {username}',
                         'token': token}},
                           {
            'response': {'type': 'error',
                         'message':
                         'Invalid password or username already taken'}}]
        assert join_response in expected_outputs
        return token, send, recv


def test_send_direct_message():
    """
    This method tests the send_direct_message method of the
    ds_protocol module. It checks if the direct message is
    sent correctly and returns the expected output.

    Args:
        None.

    Returns:
        None.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    s_token = join_server('DudeItsCesar',
                          'Damian3102')[0]
    f_token = join_server('DudeItsCesar',
                          'Damian4102')[0]
    s_direct_message = ds_protocol.send_direct_message(
                     s_token, 'Hello World!', 'ohhimark')
    f_direct_message = ds_protocol.send_direct_message(
                     f_token, 'Hello World!', 'ohhimark')
    s_str_to_dict_dm = json.loads(s_direct_message)
    f_str_to_dict_dm = json.loads(f_direct_message)
    expected_outputs = [
        '{"token": "233a1e99-d1dc-4f31-a3ba-7005117ce4e9", ' +
        '"directmessage": ' +
        '{"entry": "Hello World!", ' +
        '"recipient": "ohhimark", ' +
        f'"timestamp": "{s_str_to_dict_dm["directmessage"]["timestamp"]}"}}}}',
        '{"token": "", ' +
        '"directmessage": ' +
        '{"entry": "Hello World!", ' +
        '"recipient": "ohhimark", ' +
        f'"timestamp": "{f_str_to_dict_dm["directmessage"]["timestamp"]}"}}}}']
    assert s_direct_message == expected_outputs[0]
    assert f_direct_message == expected_outputs[1]


def test_request_new_messages():
    """
    A method to test the request_direct_messages() function in the ds_protocol
    module.

    Args:
        None

    Returns:
        None

    Raises:
        AssertionError: If any of the assertions fail.
    """
    s_token = join_server('DudeItsCesar', 'Damian3102')[0]
    f_token = join_server('DudeItsCesar', 'Damian4102')[0]
    s_new_messages = ds_protocol.request_direct_messages(
                     s_token, 'new')
    f_new_messages = ds_protocol.request_direct_messages(
                     f_token, 'new')
    f2_new_messages = ds_protocol.request_direct_messages(
                     s_token, '')
    f3_new_messages = ds_protocol.request_direct_messages(
                     s_token, 'abc123')
    expected_outputs = [
        '{"token": "233a1e99-d1dc-4f31-a3ba-7005117ce4e9", ' +
        '"directmessage": "new"}',
        '{"token": "", ' +
        '"directmessage": "new"}',
        '{"token": "233a1e99-d1dc-4f31-a3ba-7005117ce4e9", ' +
        '"directmessage": ""}',
        '{"token": "233a1e99-d1dc-4f31-a3ba-7005117ce4e9", ' +
        '"directmessage": "abc123"}']
    assert s_new_messages == expected_outputs[0]
    assert f_new_messages == expected_outputs[1]
    assert f2_new_messages == expected_outputs[2]
    assert f3_new_messages == expected_outputs[3]


def test_request_all_messages():
    """
    Test the request_direct_messages() method of the ds_protocol
    module with different parameters.

    The method sends a request to get all direct messages of
    different users, including an empty parameter and a random
    string parameter. Then, it compares the expected output with
    the actual output of the method.

    Args:
        None

    Returns:
        None

    Raises:
        AssertionError: If any of the test cases fails.
    """
    s_token = join_server('DudeItsCesar', 'Damian3102')[0]
    f_token = join_server('DudeItsCesar', 'Damian4102')[0]
    s_all_messages = ds_protocol.request_direct_messages(
                     s_token, 'all')
    f_all_messages = ds_protocol.request_direct_messages(
                     f_token, 'all')
    f2_all_messages = ds_protocol.request_direct_messages(
                     s_token, '')
    f3_all_messages = ds_protocol.request_direct_messages(
                     s_token, 'abc123')
    expected_outputs = [
        '{"token": "233a1e99-d1dc-4f31-a3ba-7005117ce4e9", ' +
        '"directmessage": "all"}',
        '{"token": "", ' +
        '"directmessage": "all"}',
        '{"token": "233a1e99-d1dc-4f31-a3ba-7005117ce4e9", ' +
        '"directmessage": ""}',
        '{"token": "233a1e99-d1dc-4f31-a3ba-7005117ce4e9", ' +
        '"directmessage": "abc123"}']
    assert s_all_messages == expected_outputs[0]
    assert f_all_messages == expected_outputs[1]
    assert f2_all_messages == expected_outputs[2]
    assert f3_all_messages == expected_outputs[3]


def test_direct_message_response():
    """
    Tests the response of the direct message protocol.

    This method tests the response of the direct message
    protocol by joining two servers and sending direct messages
    between them. It then verifies that the responses received
    from the servers match the expected output.

    Args:
        None

    Returns:
        None.

    Raises:
        AssertionError: If the responses received from the
                        servers do not match the expected output.
    """
    s_token, s_send, s_recv = join_server('DudeItsCesar', 'Damian3102')
    f_token, f_send, f_recv = join_server('DudeItsCesar', 'Damian4102')
    s_direct_message = ds_protocol.send_direct_message(
                       s_token, 'Hello World!', 'ohhimark')
    s_send.write(s_direct_message + '\r\n')
    s_send.flush()
    recv_dm = s_recv.readline()[:-1]
    s_response = ds_protocol.extract_direct_message(recv_dm)
    s_response = s_response.response

    f_direct_message = ds_protocol.send_direct_message(
                       f_token, 'Hello World!', 'ohhimark')
    f_send.write(f_direct_message + '\r\n')
    f_send.flush()
    recv_dm = f_recv.readline()[:-1]
    f_response = ds_protocol.extract_direct_message(recv_dm)
    f_response = f_response.response

    expected_outputs = [{
        'response': {'type': 'ok',
                     'message': 'Direct message sent'}},
                        {
        'response': {'type': 'error',
                     'message': 'Post rejected: invalid token'}}]
    assert s_response == expected_outputs[0]
    assert f_response == expected_outputs[1]


def test_all_new_messages():
    """
    This method tests the 'request_direct_messages' function of the
    'ds_protocol' module. It joins a server with two different users
    and sends requests for new and all direct messages using the
    'request_direct_messages' function. It then extracts and verifies
    the responses received from the server.

    Args:
        None

    Returns:
        None

    Raises:
        AssertionError: If the responses received from the
                        servers do not match the expected output.
    """
    s_token, s_send, s_recv = join_server('Trout', 'Damian3102')
    f_token, f_send, f_recv = join_server('Trout', 'Damian4102')

    s_new_messages = ds_protocol.request_direct_messages(
                   s_token, 'new')
    s_send.write(s_new_messages + '\r\n')
    s_send.flush()
    s_new_msg_response = ds_protocol.extract_direct_message(
                         s_recv.readline()[:-1])
    s_request_response = s_new_msg_response.response

    s2_all_messages = ds_protocol.request_direct_messages(
                      s_token, 'all')
    s_send.write(s2_all_messages + '\r\n')
    s_send.flush()
    s2_new_msg_response = ds_protocol.extract_direct_message(
                          s_recv.readline()[:-1])
    s2_request_response = s2_new_msg_response.response

    f_new_messages = ds_protocol.request_direct_messages(
                     f_token, 'new')

    f_send.write(f_new_messages + '\r\n')
    f_send.flush()
    f_new_msg_response = ds_protocol.extract_direct_message(
                         f_recv.readline()[:-1])
    f_request_response = f_new_msg_response.response

    f2_all_messages = ds_protocol.request_direct_messages(
                      s_token, '')
    f_send.write(f2_all_messages + '\r\n')
    f_send.flush()
    f2_new_msg_response = ds_protocol.extract_direct_message(
                          f_recv.readline()[:-1])
    f2_request_response = f2_new_msg_response.response

    expected_outputs = [{
        'response': {'type': 'ok',
                     'messages': []}},
                        {
        'response': {'type': 'ok',
                     'messages':
                     [{'message': 'Hey Trout!',
                       'from': 'Shohei',
                       'timestamp': '1679642089.112004'},
                      {'message': 'How are ya!',
                       'from': 'Shohei',
                       'timestamp': '1679642093.3296661'}]}},
                        {
        'response': {'type': 'error',
                     'message': 'Post rejected: invalid token'}},
                        {
        'response': {'type': 'error',
                     'message': 'Unable to decrypt post entry.'}}]
    assert s_request_response == expected_outputs[0]
    assert s2_request_response == expected_outputs[1]
    assert f_request_response == expected_outputs[2]
    assert f2_request_response == expected_outputs[3]
