import unittest
from commands_handler import CommandsHandler


class TestCommandsHandler(unittest.TestCase):

    def test_non_admin_user_input(self):
        commands_handler = CommandsHandler()
        self.assertRaises(Exception, commands_handler.input_command("/test aaa"))
        self.assertRaises(Exception, commands_handler.input_command("/test aaaaa bbbb ccc"))
        self.assertRaises(Exception, commands_handler.input_command("/test aaa bb"))
        self.assertRaises(Exception, commands_handler.input_command(""))
        self.assertRaises(Exception, commands_handler.input_command("/auth"))
        self.assertRaises(Exception, commands_handler.input_command("/auth a"))
        self.assertRaises(Exception, commands_handler.input_command("/auth a b b b "))
        self.assertRaises(Exception, commands_handler.input_command("/auth ccccc c ccc c c 22"))
        self.assertRaises(Exception, commands_handler.input_command("/get_users 1"))
        self.assertRaises(Exception, commands_handler.input_command("/get_users"))
        self.assertRaises(Exception, commands_handler.input_command("/add_user"))
        self.assertRaises(Exception, commands_handler.input_command("/add_user a a a a"))

    def test_admin_user_input(self):
        commands_handler = CommandsHandler()
        self.assertRaises(Exception, commands_handler.input_command("/auth admin 1"))
        self.assertRaises(Exception, commands_handler.input_command("/test aaa"))
        self.assertRaises(Exception, commands_handler.input_command("/test aaaaa bbbb ccc"))
        self.assertRaises(Exception, commands_handler.input_command("/test aaa bb"))
        self.assertRaises(Exception, commands_handler.input_command(""))
        self.assertRaises(Exception, commands_handler.input_command("/get_users 1"))
        self.assertRaises(Exception, commands_handler.input_command("/get_users"))
        self.assertRaises(Exception, commands_handler.input_command("/add_user"))
        self.assertRaises(Exception, commands_handler.input_command("/add_user a a a a"))
        self.assertRaises(Exception, commands_handler.input_command("/delete_user 1 1"))
        self.assertRaises(Exception, commands_handler.input_command("/delete_user 10"))
        self.assertRaises(Exception, commands_handler.input_command("/add_user aaaaa sss b"))
