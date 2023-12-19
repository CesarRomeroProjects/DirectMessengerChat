"""
The module is a unit test suite for the Profile class. It contains
test cases for saving and loading profile data to/from a DSU file,
as well as error cases for invalid file paths and file types.

The Profile class is imported from the Profile module, as well as
the DsuFileError exception. The unittest module is also imported to
define test cases. The tempfile and pathlib modules are imported to
create temporary directories and files for testing.

The TestProfile class contains four test cases. The setUp method
initializes a Profile instance with default values for dsuserver,
username, and password properties. It also adds two contacts with
names 'Timmy' and 'Billy' respectively to the users property.
Additionally, it adds three messages sent by 'Harambe' to the
user_msgs property and three messages received by 'Harambe' to the
recipient_msgs property.
"""
# NAME: Cesar Damian Romero Amador
# EMAIL: cesardr1@uci.edu
# STUDENT ID: 31358030
import unittest
import tempfile
from pathlib import Path
from Profile import Profile
from Profile import DsuFileError


class TestProfile(unittest.TestCase):
    """
    A unit test suite for the Profile class.

    The suite contains test cases for saving and
    loading profile data to/from a DSU file, as well
    as error cases for invalid file paths and file types.

    The setUp method initializes a Profile instance with
    default values for dsuserver, username, and password
    properties. It also adds two contacts with names
    'Timmy' and 'Billy' respectively to the users property.
    Additionally, it adds three messages sent by 'Harambe'
    to the user_msgs property and three messages received
    by 'Harambe' to the recipient_msgs property.
    """
    def setUp(self):
        """
        Initializes a Profile instance with default values for
        dsuserver, username and password properties. Adds two
        contacts with names 'Timmy' and 'Billy' respectively to
        the users property. Adds three messages sent by 'Harambe'
        to the user_msgs property and three messages received by
        'Harambe' to the recipient_msgs property.
        """
        self.profile = Profile(dsuserver="127.0.0.1",
                               username="Harambe",
                               password="testpassword")
        self.profile.add_contact(
            ['Timmy', 'Harambe'])
        self.profile.add_contact(
            ['Billy', 'Harambe'])
        self.profile.user_messages(
            ['Harambe', 'Hey!', 'Timmy', 'testtime'])
        self.profile.user_messages(
            ['Harambe', 'I\'m good!', 'Timmy', 'testtime'])
        self.profile.user_messages(
            ['Harambe', 'Hey Billy!', 'Billy', 'testtime'])
        self.profile.recipient_messages(
            ['Timmy', 'Hey Harambe!', 'Harambe', 'testtime'])
        self.profile.recipient_messages(
            ['Timmy', 'How are you?', 'Harambe', 'testtime'])
        self.profile.recipient_messages(
            ['Billy', 'Hey Harambe', 'Harambe', 'testtime'])

    def test_save_and_load_profile(self):
        """
        This function tests the ability of the Profile class to save and
        load profile data to/from a dsu file. The function creates a
        temporary directory and a new file in that directory. It then saves
        the current instance of the Profile class to the file and creates a
        new instance of the Profile class. The new instance is then populated
        with data from the saved dsu file. The function then asserts that the
        data in the new instance matches the expected values.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_profile.dsu"
            filepath.touch()
            self.profile.save_profile(filepath)

            new_profile = Profile()
            new_profile.load_profile(filepath)

            self.assertEqual(new_profile.dsuserver, "127.0.0.1")
            self.assertEqual(new_profile.username, "Harambe")
            self.assertEqual(new_profile.password, "testpassword")
            self.assertEqual(new_profile.users,
                             [['Timmy', 'Harambe'],
                              ['Billy', 'Harambe']])
            self.assertEqual(new_profile.user_msgs,
                             [['Harambe', 'Hey!', 'Timmy', 'testtime'],
                              ['Harambe', 'I\'m good!', 'Timmy', 'testtime'],
                              ['Harambe', 'Hey Billy!', 'Billy', 'testtime']])
            self.assertEqual(new_profile.recipient_msgs,
                             [['Timmy', 'Hey Harambe!', 'Harambe', 'testtime'],
                              ['Timmy', 'How are you?', 'Harambe', 'testtime'],
                              ['Billy', 'Hey Harambe', 'Harambe', 'testtime']])

    def test_save_profile_with_invalid_path(self):
        """
        This test case verifies that attempting to save a Profile object
        to an invalid path raises a DsuFileError. The test calls the
        save_profile function of the Profile class with an invalid path
        and asserts that a DsuFileError is raised.
        """
        with self.assertRaises(DsuFileError):
            self.profile.save_profile(
                'path/lol/lol/nonexistant/test_profile.dsu')

    def test_load_profile_with_invalid_path(self):
        """
        This function tests the load_profile method of the Profile class
        when the specified file path is invalid.
        """
        with self.assertRaises(DsuFileError):
            self.profile.load_profile(
                'path/lol/lol/nonexistant/test_profile.dsu')

    def test_load_profile_with_invalid_file_type(self):
        """
        This function tests the behavior of the Profile.load_profile method
        when an invalid file type is provided. It creates a temporary file
        with a '.txt' suffix and attempts to load it as a DSU file. The
        function expects a DsuFileError to be raised since the file type
        is invalid.
        """
        with tempfile.NamedTemporaryFile(suffix='.txt') as tmpfile:
            with self.assertRaises(DsuFileError):
                self.profile.load_profile(Path(tmpfile.name))


if __name__ == "__main__":
    unittest.main()
