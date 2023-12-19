# NAME: Cesar Damian Romero Amador
# EMAIL: cesardr1@uci.edu
# STUDENT ID: 31358030
import tkinter as tk
import time
from tkinter import ttk, filedialog, messagebox
from typing import Text
from profile import Profile, DsuFileError, DsuProfileError
from ds_messenger import DirectMessenger
from ds_messenger import CannotConnectToServer
from ds_messenger import InvalidJoinMessage


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self.last_msg = 0.0
        self._draw()

    def node_select(self, event):
        selected_items = self.posts_tree.selection()
        if selected_items:
            index = int(selected_items[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        num_id = len(self._contacts) - 1
        self._insert_contact_tree(num_id, contact)

    def _insert_contact_tree(self, num_id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        num_id = self.posts_tree.insert('', num_id, num_id, text=contact)

    def insert_user_message(self, message: str):
        self.last_msg += 1.0
        self.entry_editor.insert(self.last_msg, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        self.last_msg += 1.0
        self.entry_editor.insert(self.last_msg, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)

        tk.Label(master=self, text="Contacts", width=22).place(x=2,
                                                               y=6)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.config(command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None,
                 user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show="*")
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.dsu_file = None
        self.recipients = []
        self.recipient_msgs = []
        self.user_msgs = []
        self.direct_messenger = DirectMessenger(self.server,
                                                self.username,
                                                self.password)
        self._draw()

    def open_file(self):
        profile = Profile()
        self.recipient = None
        self.recipient_msgs = []
        self.user_msgs = []
        contacts = self.body.posts_tree.get_children()
        for contact in contacts:
            self.body.posts_tree.delete(contact)
        try:
            self.dsu_file = filedialog.askopenfilename(
                title="Select A DSU File",
                filetypes=(("dsu files", "*.dsu"),))
            profile.load_profile(self.dsu_file)
            self.username = profile.username
            self.password = profile.password
            self.server = profile.dsuserver
            self.direct_messenger.username = self.username
            self.direct_messenger.password = self.password
            self.direct_messenger.dsuserver = self.server
            self.contact_list(profile)
            for msg in profile.recipient_msgs:
                self.recipient_msgs.append(msg)
            for msg in profile.user_msgs:
                self.user_msgs.append(msg)
        except (DsuFileError, DsuProfileError):
            pass

    def new_file(self):
        profile = Profile()
        self.recipient = None
        self.recipient_msgs = []
        self.user_msgs = []
        contacts = self.body.posts_tree.get_children()
        for contact in contacts:
            self.body.posts_tree.delete(contact)
        profile.dsuserver = tk.simpledialog.askstring(
                            'New Profile',
                            'Enter Server Address: ')
        profile.username = tk.simpledialog.askstring(
                            'New Profile',
                            'Enter Username: ')
        profile.add_usernames(profile.username)
        profile.password = tk.simpledialog.askstring(
                            'New Profile',
                            'Enter Password: ')
        self.dsu_file = filedialog.asksaveasfilename(
                            defaultextension=".*",
                            title="Save File",
                            filetypes=(("DSU Files",
                                        "*.dsu"),))
        if self.dsu_file:
            with open(self.dsu_file, "w", encoding='utf-8'):
                pass
            self.username = profile.username
            self.password = profile.password
            self.server = profile.dsuserver
            self.direct_messenger.username = self.username
            self.direct_messenger.password = self.password
            self.direct_messenger.dsuserver = self.server
            profile.save_profile(self.dsu_file)

    def close_file(self):
        if self.dsu_file:
            profile = Profile()
            profile.load_profile(self.dsu_file)
            info_retrieved = []
            for username in profile.usernames:
                if username not in info_retrieved:
                    info_retrieved.append(username)
                    self.direct_messenger = DirectMessenger(
                                            self.server,
                                            username,
                                            self.password)
                    messages = self.direct_messenger.retrieve_all()
                    if messages:
                        for user_msg in messages:
                            recipient = user_msg.recipient
                            message = user_msg.message
                            host = username
                            msg_time = user_msg.timestamp
                            msg_obj = [recipient, message,
                                       host, msg_time]
                            if msg_obj not in profile.recipient_msgs:
                                profile.recipient_messages(msg_obj)
                    profile.save_profile(self.dsu_file)
            self.root.destroy()
            self.root.quit()
        else:
            self.root.destroy()
            self.root.quit()

    def _error_message(self, error: str) -> None:
        top = tk.Toplevel(self.root)
        top.geometry("350x150")
        top.title("Error Message")
        label = tk.Label(top,
                         text=error,
                         font="Arial 17 bold")
        label.place(relx=0.5, rely=0.5, anchor="center")

    def send_message(self):
        """
        Sends a message to the specified recipient.
        If the recipient exists, the method creates a profile object
        and loads the user's profile. It then gets the message from the
        text entry box, sends the message using the direct_messenger
        object, and saves the sent message in the user's profile. The
        sent message is also appended to the user's messages list and
        the profile is saved. The message is displayed in the GUI with
        a [YOU] tag to indicate that it was sent by the user. If the
        message fails to send, the user is prompted to configure their
        settings.

        Returns:
            None
        """
        if self.recipient:
            profile = Profile()
            profile.load_profile(self.dsu_file)
            message = self.body.get_text_entry()
            msg_sent = self.direct_messenger.send(
                       message,
                       self.recipient)
            if msg_sent:
                msg_obj = [self.username,
                           message,
                           self.recipient,
                           time.time()]
                profile.user_messages(msg_obj)
                self.user_msgs.append(msg_obj)
                profile.save_profile(self.dsu_file)
                self.body.insert_user_message(message + '[YOU]')
                self.body.message_editor.delete(1.0, tk.END)
            else:
                answer = messagebox.askquestion(
                    'Unable To Join Server',
                    'Cannot send message!\n' +
                    'Username or password\n' +
                    'does not meet\n' +
                    'server requirements!\n' +
                    'Would you like to configure your settings?')
                if answer == 'yes':
                    self.configure_server()

    def add_contact(self):
        """
        Prompt the user to enter a new contact name and add it to the list
        of contacts in the application's body. Also adds the contact to the
        user's profile. If the user hasn't loaded or created a DSU file, an
        error message will be displayed.

        Raises:
            AttributeError: If the user hasn't loaded or created a DSU file.
        """
        if self.dsu_file:
            profile = Profile()
            profile.load_profile(self.dsu_file)
            name = tk.simpledialog.askstring('New User',
                                             'Enter the name of new user: ')
            self.body.insert_contact(name)
            profile.add_contact([name, self.username])
            profile.save_profile(self.dsu_file)

    def recipient_selected(self, recipient):
        """
        Load the profile, set the selected recipient, clear the message
        entry editor, and display the messages exchanged between the
        current user and the selected recipient.

        Args:
            recipient (str): The username of the recipient.

        Returns:
            None
        """
        profile = Profile()
        profile.load_profile(self.dsu_file)
        self.recipient = recipient
        self.body.entry_editor.delete(1.0, tk.END)
        msgs = []
        for msg in self.recipient_msgs:
            if msg[0] == recipient:
                msgs.append(msg)
        for msg in self.user_msgs:
            if msg[2] == recipient:
                msgs.append(msg)
        sorted_list = sorted(msgs, key=lambda x: float(x[3]))
        for msg in sorted_list:
            if msg[0] == recipient:
                self.body.insert_contact_message(f'[{recipient}]' + msg[1])
            elif msg[0] in profile.usernames:
                if msg[2] == recipient:
                    self.body.insert_user_message(msg[1] + f'[YOU]')

    def configure_server(self):
        """
        Configure server function.

        This function is used to configure the account by getting
        the username, password, and server from the user using the
        NewContactDialog class. It updates the instance variables of
        the class with the new values and saves the new configuration
        to the profile.

        Args:
            self (object): An instance of the class.

        Returns:
            None
        """
        if self.dsu_file:
            u_d = NewContactDialog(self.root, "Configure Account",
                                   self.username, self.password, self.server)
            self.username = u_d.user
            self.password = u_d.pwd
            self.server = u_d.server
            self.direct_messenger = DirectMessenger(
                self.server,
                self.username,
                self.password)
            profile = Profile()
            profile.load_profile(self.dsu_file)
            profile.username = self.username
            profile.add_usernames(profile.username)
            profile.password = self.password
            profile.dsuserver = self.server
            profile.save_profile(self.dsu_file)
            self.check_new()

    def check_new(self):
        try:
            if self.recipient:
                recipient_msgs = self.direct_messenger.retrieve_new()
                reversed_list = reversed(recipient_msgs)
                if reversed_list:
                    profile = Profile()
                    profile.load_profile(self.dsu_file)
                    lst_msgs = []
                    if self.recipient_msgs:
                        last_msgs = self.recipient_msgs[
                            -len(self.recipient_msgs):]
                    else:
                        last_msgs = []
                    for obj in reversed_list:
                        contact = obj.recipient
                        contact_msg = obj.message
                        contact_time = obj.timestamp
                        msg = [contact,
                               contact_msg,
                               self.username,
                               contact_time]
                        if not any(msg == last_msg for last_msg in last_msgs):
                            self.recipient_msgs.append(msg)
                            self.body.insert_contact_message(
                                f'[{self.recipient}]' + contact_msg)
                            last_msgs.append(msg)
                            if len(last_msgs) > len(self.recipient_msgs):
                                last_msgs.pop(0)
                    profile.save_profile(self.dsu_file)
            self.root.after(1000, self.check_new)
        except TypeError:
            pass
        except CannotConnectToServer:
            answer = messagebox.askquestion(
                'ERROR', 'Cannot connect to server\n' +
                         'Would you like to configure server IP?\n' +
                         'or\n' +
                         'Quit the application?')
            if answer == 'yes':
                self.configure_server()
            else:
                self.root.destroy()
                self.root.quit()
        except InvalidJoinMessage:
            answer = messagebox.askquestion(
                'Unable To Join Server',
                'Cannot update message(s)!\n' +
                'Username or password\n' +
                'does not meet\n' +
                'server requirements!\n' +
                'Would you like to configure your settings?')
            if answer == 'yes':
                self.configure_server()
            else:
                pass

    def contact_list(self, profile):
        """
        Displays a list of contacts in the user interface,
        using the profile provided.

        Args:
            profile: a Profile object that contains
            information about the user's contacts.

        Returns:
            None
        """
        for contact in profile.users:
            self.body.insert_contact(contact[0])

    def _draw(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New',
                              command=self.new_file)
        menu_file.add_command(label='Open...',
                              command=self.open_file)
        menu_file.add_command(label='Close',
                              command=self.close_file)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
