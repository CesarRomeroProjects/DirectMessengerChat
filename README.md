# Direct Messenger Chat

# Overview
This project, named Social Messenger, is a direct messaging application integrated with the DSP platform. The goal is to allow students to communicate with each other using a dedicated messaging module. The project is divided into several parts, each building upon the previous one.

# Part 1: Implementing the Direct Messaging Protocol
In this section, the ds_protocol module is extended to support direct messaging. The protocol includes commands like directmessage, allowing users to send and retrieve messages. The communication with the DSP server is facilitated through JSON messages. The module includes parsing functions to handle different types of messages.

Testing

A dedicated testing module (test_ds_message_protocol.py) is provided to validate the correct processing of the implemented protocol. Test cases cover scenarios such as sending direct messages, requesting unread messages, and obtaining all messages.

# Part 2: The DS Direct Messenger Module
The ds_messenger module is introduced in this part, providing classes to manage direct messaging functionalities. It includes a DirectMessenger class with methods to send messages, retrieve new messages, and retrieve all messages. The module is designed to function independently without external dependencies.

Testing

A testing module (test_ds_messenger.py) is created to ensure the correct functioning of the ds_messenger module. Test cases cover sending messages, retrieving new and all messages, and handling edge cases.

# Part 3: Storing Messages Locally
The project focuses on storing message data locally to enhance user experience. The profile module is extended to support serializing new data, enabling the program to display messages and recipients without requiring an internet connection. This feature ensures that previous interactions are preserved across program launches.

# Part 4: The Graphical User Interface (GUI)
The final part involves creating a graphical user interface using Tkinter. The GUI allows users to interact with the messaging module seamlessly. It includes features such as a user treeview, message display, text input for new messages, and buttons for adding users and sending messages. The GUI automatically retrieves new messages while the program is running and visually separates conversations.

Additional Requirements
- GUI Design: While the provided wireframe is a suggestion, the GUI layout should be intuitive and user-friendly. Visual separation of conversations is necessary.
- Automatic Message Retrieval: The GUI should automatically fetch new messages while the program is running, providing real-time updates.
- Conversation Separation: Conversations in the GUI should be visually separated, ensuring clarity for users.

Testing

Testing the GUI involves ensuring that the user interface responds correctly to user actions, such as selecting users, sending messages, and adding new contacts. Unit tests for GUI components are recommended.

# How to Run the Program
1. Ensure Python is installed on your system.
2. Extract the provided zip file (Assignment5.zip).
3. Navigate to the project directory using the terminal.
4. Run the program by executing python a5.py.
5. Follow the on-screen instructions to interact with the Social Messenger application.