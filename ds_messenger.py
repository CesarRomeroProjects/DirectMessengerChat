# NAME: Cesar Damian Romero Amador
# EMAIL: cesardr1@uci.edu
# STUDENT ID: 31358030
import socket
import ds_protocol as protocol


class CannotConnectToServer(Exception):
    """
    Exception raised when a connection to a server cannot be established.
    """


class NoUser(Exception):
    """
    An exception class to be raised when no user is found in the system.
    """


class InvalidJoinMessage(Exception):
    """
    An exception class to be raised when user cannot join server due
    to invalid username or wrong password
    """


class DirectMessage:
    """
    A class to represent a direct message.

    Attributes:
      recipient (str or None): The recipient of the message.
      message (str or None): The content of the message.
      timestamp (datetime.datetime or None): The timestamp of
                                             the message.
    """
    def __init__(self):
        """
        Initialize a DirectMessage object with recipient, message, and
        timestamp.

        Args:
          None

        Attributes:
          recipient (str): The recipient of the direct message.
          message (str): The content of the direct message.
          timestamp (datetime): The timestamp when the direct message was
                                sent.
        """
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """
    A class that allows sending and receiving of direct messages
    through a server.

    Args:
        dsuserver (str): The server address.
        username (str): The username to connect with.
        password (str): The password to authenticate the user.

    Attributes:
        token (str): The authentication token received upon successful
                     authentication.
        dsuserver (str): The server address.
        username (str): The username to connect with.
        password (str): The password to authenticate the user.

    Methods:
        send(message: str, recipient: str) -> bool:
            Sends a direct message to the specified recipient.
            Returns True if the message was successfully sent, False if
            send failed.

        retrieve_new() -> list:
            Retrieves a list of DirectMessage objects containing all
            new messages.

        retrieve_all() -> list:
            Retrieves a list of DirectMessage objects containing all
            messages.

        join_server(dsuserver: str, username: str, password: str):
            Establishes a connection to the specified server and returns
            the send, receive, andresponse objects.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        """
        Initialize the DirectMessenger instance.

        Args:
            dsuserver (str): The server address.
            username (str): The username to connect with.
            password (str): The password to authenticate the user.
        """
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.all_msgs = []
        self.new_msgs = []

    def send(self, message: str, recipient: str) -> bool:
        """
        Sends a direct message to the specified recipient.

        Args:
            message (str): The message to send.
            recipient (str): The username of the recipient.

        Returns:
            bool: True if the message was successfully sent,
                  False if send failed.
        """
        try:
            # must return true if message successfully sent, otherwise false.
            send, recv, response = self.join_server(
                                   self.dsuserver,
                                   self.username,
                                   self.password)
            response_type = response['response']['type']
            # Confirms Joining Server
            print(response)
            if response_type == 'ok':
                self.token = response['response']['token']
                if message == '' or recipient == '':
                    return False
                direct_msg = protocol.send_direct_message(
                                      self.token,
                                      message,
                                      recipient)
                # Shows What Was Sent
                print(direct_msg)
                send.write(direct_msg + '\r\n')
                send.flush()
                response = protocol.parse_direct_message(
                                    recv.readline()[:-1])
                response = response.response
                # Confirms Direct Message Was Sent
                print(response)
                response_type = response['response']['type']
                return bool(response_type == 'ok')
            return False
        except (CannotConnectToServer, KeyError):
            return False
        except NoUser:
            return False

    def retrieve_new(self) -> list:
        """
        Retrieves a list of DirectMessage objects containing all
        new messages.

        Returns:
            list: A list of DirectMessage objects containing all
                  new messages.
        """
        # must return a list of DirectMessage objects containing all new
        # messages
        send, recv, response = self.join_server(
                                self.dsuserver,
                                self.username,
                                self.password
                                )
        join_status = response['response']['type']
        print(response)
        if join_status == 'ok':
            self.token = response['response']['token']
            recv_msgs = protocol.request_direct_messages(
                                 self.token,
                                 'new'
                                 )
            send.write(recv_msgs + '\r\n')
            send.flush()
            response = protocol.parse_direct_message(
                                recv.readline()[:-1]
                                )
            response = response.response
            dm_status = response['response']['type']
            print(response)
            if dm_status == 'ok':
                for msg in response['response']['messages']:
                    dm_obj = DirectMessage()
                    dm_obj.recipient = msg['from']
                    dm_obj.message = msg['message']
                    dm_obj.timestamp = float(msg['timestamp'])
                    self.new_msgs.append(dm_obj)
                return sorted(self.new_msgs,
                              key=lambda
                              dm_obj: dm_obj.timestamp,
                              reverse=True)
        else:
            raise InvalidJoinMessage

    def retrieve_all(self) -> list:
        """
        Retrieve all DirectMessages from the server.

        Returns:
          A list of DirectMessage objects containing all messages.
        """
        # must return a list of DirectMessage objects containing all messages
        send, recv, response = self.join_server(
                               self.dsuserver,
                               self.username,
                               self.password
                               )
        join_status = response['response']['type']
        if join_status == 'ok':
            self.token = response['response']['token']
            recv_msgs = protocol.request_direct_messages(
                                 self.token,
                                 'all'
                                 )
            send.write(recv_msgs + '\r\n')
            send.flush()
            response = protocol.parse_direct_message(
                                recv.readline()[:-1]
                                )
            response = response.response
            dm_status = response['response']['type']
            if dm_status == 'ok':
                for msg in response['response']['messages']:
                    dm_obj = DirectMessage()
                    dm_obj.recipient = msg['from']
                    dm_obj.message = msg['message']
                    dm_obj.timestamp = float(msg['timestamp'])
                    self.all_msgs.append(dm_obj)
            return sorted(self.all_msgs,
                              key=lambda
                              dm_obj: dm_obj.timestamp,
                              reverse=True)

    def join_server(self, dsuserver, username, password):
        """
        Join a server with the specified username and password.

        Args:
          dsuserver (str): The DsuServer hostname or IP address.
          username (str): The username to use for joining the server.
          password (str): The password to use for joining the server.

        Returns:
          Tuple: A tuple containing the send and receive file objects, and
          the response from the server as a JSON object.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((dsuserver, 3021))
                send = client.makefile('w')
                recv = client.makefile('r')
                join = protocol.join_command(username, password)
                send.write(join + '\r\n')
                send.flush()
                response = protocol.extract_json(recv.readline()[:-1])
                return send, recv, response.response
        except (BlockingIOError, ConnectionRefusedError) as exc:
            raise CannotConnectToServer from exc
        except (OSError, TimeoutError) as exc:
            raise CannotConnectToServer from exc
