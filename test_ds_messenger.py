# NAME: Cesar Damian Romero Amador
# EMAIL: cesardr1@uci.edu
# STUDENT ID: 31358030
"""
This module contains three test functions for the ds_messenger.DirectMessenger
class: test_send, test_retrieve_new, and test_retrieve_all.

test_send tests the send method of DirectMessenger by creating eight instances
of the class with different arguments and testing the send method of each
instance. It asserts whether each message is sent successfully to the intended
recipient.

test_retrieve_new retrieves and tests new direct messages from a
DirectMessenger instance by calling the retrieve_new method. It asserts that
the returned value is a list of DirectMessage instances.

test_retrieve_all tests the retrieve_all method of DirectMessenger by calling
the method and asserting that the returned value is a list of DirectMessage
instances.
"""
from ds_messenger import DirectMessenger, DirectMessage


def test_send():
    """
    Test the send method of DirectMessenger class.

    This function creates eight instances of the DirectMessenger class with
    different arguments and tests the send method of each instance. It asserts
    whether each message is sent successfully to the intended recipient.

    Args:
        None

    Returns:
        None

    Raises:
        AssertionError: If any of the assertions fail.
    """
    test1 = DirectMessenger('168.235.86.101', 'DudeItsCesar', 'Damian3102')
    test2 = DirectMessenger('sefsefse', 'DudeItsCesar', 'Damian3102')
    test3 = DirectMessenger('124.65.73.79', 'DudeItsCesar', 'Damian3102')
    test4 = DirectMessenger('', 'DudeItsCesar', 'Damian3102')
    test5 = DirectMessenger('168.235.86.101', '', 'Damian3102')
    test6 = DirectMessenger('168.235.86.101', 'DudeItsCesar', '')
    test7 = DirectMessenger('168.235.86.101', '', '')
    test8 = DirectMessenger('168.235.86.101')
    assert test1.send('Hello World!', 'KianaDiana') is True
    assert test1.send('', 'KianaDiana') is False
    assert test1.send('Hello World!', '') is False
    assert test1.send('', '') is False
    assert test2.send('Hello World!', 'KianaDiana') is False
    assert test3.send('Hello World!', 'KianaDiana') is False
    assert test4.send('Hello World!', 'KianaDiana') is False
    assert test5.send('Hello World!', 'KianaDiana') is False
    assert test6.send('Hello World!', 'KianaDiana') is False
    assert test7.send('Hello World!', 'KianaDiana') is False
    assert test8.send('Hello World!', 'KianaDiana') is False


def test_retrieve_new():
    """
    Retrieve and test new direct messages from a DirectMessenger instance.

    Args:
        None

    Returns:
        None

    Raises:
        AssertionError: If any of the assertions fail.
    """
    test = DirectMessenger('168.235.86.101', 'DudeItsCesar', 'Damian3102')
    dm_list = test.retrieve_new()
    assert isinstance(dm_list, list)
    for msg in dm_list:
        assert isinstance(msg, DirectMessage)


def test_retrieve_all():
    """
    Test function for retrieving all DirectMessages from a
    DirectMessenger instance.

    Args:
        None

    Returns:
        None, but raises an AssertionError if:
        - The returned value from DirectMessenger.retrieve_all() is not a list.
        - Any element in the returned list is not an instance of DirectMessage.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    test = DirectMessenger('168.235.86.101', 'DudeItsCesar', 'Damian3102')
    dm_list = test.retrieve_all()
    assert isinstance(dm_list, list)
    for msg in dm_list:
        assert isinstance(msg, DirectMessage)
