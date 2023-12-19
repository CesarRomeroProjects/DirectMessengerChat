"""
Module for managing DSU profiles.

This module provides a Profile class for managing user information required
to join an ICS 32 DSU server. The Profile class allows for adding contacts
and storing user and recipient messages. The class also provides methods
for saving and loading profile data to and from a DSU file.

Exceptions:
    DsuFileError: Raised when attempting to load or save Profile objects to
                  file the system.
    DsuProfileError: Raised when attempting to deserialize a dsu file to a
                     Profile object.

Classes:
    Profile: A class that exposes the properties required to join an ICS 32
             DSU server.
"""
# NAME: Cesar Damian Romero Amador
# EMAIL: cesardr1@uci.edu
# STUDENT ID: 31358030
import json
from pathlib import Path


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should
    catch in your own code. It is raised when attempting to load
    or save Profile objects to file the system.
    """


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should
    catch in your own code. It is raised when attempting to deserialize
    a dsu file to a Profile object.
    """


class Profile:
    """
    The Profile class exposes the properties required to join an
    ICS 32 DSU server. You will need to use this class to manage the
    information provided by each new user created within your program for
    a2. Pay close attention to the properties and functions in this class
    as you will need to make use of each of them in your program.

    When creating your program you will need to collect user input for the
    properties exposed by this class. A Profile class should ensure that a
    username and password are set, but contains no conventions to do so. You
    should make sure that your code verifies that required properties are set.

    """
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.usernames = []
        self.users = []
        self.user_msgs = []
        self.recipient_msgs = []

    def add_usernames(self, username):
        self.usernames.append(username)
        
    def add_contact(self, user):
        """
        The add_contact method adds a user to the list of
        contacts for the current Profile instance.

        Args:
            user: A str representing the username of the
                  user to add as a contact.

        Returns:
            None
        """
        self.users.append(user)

    def user_messages(self, msgs):
        """
        Add a list of user messages to the current
        instance of the Profile object.

        Args:
            msgs: a list of user messages to add to
                  the current Profile object.

        Returns:
            None
        """
        self.user_msgs.append(msgs)

    def recipient_messages(self, msgs):
        """
        Add messages to the recipient messages list.

        Args:
            msgs: A message or list of messages to
                  be added to the recipient messages
                  list.

        Returns:
            None
        """
        self.recipient_msgs.append(msgs)

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance
        of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError
        """
        path_obj = Path(path)

        if path_obj.exists() and path_obj.suffix == '.dsu':
            try:
                with open(path_obj, 'w', encoding='utf-8') as file:
                    json.dump(self.__dict__, file)
            except Exception as ex:
                raise DsuFileError(
                    "Error while attempting to process the DSU file.",
                    ex) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of Profile with data
        stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError
        """
        path_obj = Path(path)

        if path_obj.exists() and path_obj.suffix == '.dsu':
            try:
                with open(path_obj, 'r', encoding='utf-8') as file:
                    obj = json.load(file)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    for contacts in obj['users']:
                        self.users.append(contacts)
                    for msgs in obj['user_msgs']:
                        self.user_msgs.append(msgs)
                    for msgs in obj['recipient_msgs']:
                        self.recipient_msgs.append(msgs)
                    for usernames in obj['usernames']:
                        self.usernames.append(usernames)
            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()
