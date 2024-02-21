#!/usr/bin/python3
"""Test Cases for the console. NOT WORKING"""
import unittest
import os
import re
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
from models import storage


class TestDoCreate(unittest.TestCase):
    """Test cases for do_create module"""

    def setUp(self):
        """set up module"""

        self.command = HBNBCommand()

    def tearDown(self):
        """Tear down"""

        HBNBCommand.classes = {}
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_do_create_with_attributes(self):
        """Test do_create method with attributes"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.onecmd('create State name="Ekiti"')
            created_id = mock_stdout.getvalue().strip()
            self.assertIn('State.{}'.format(created_id), storage.all().keys())
            """self.clear_storage()
            self.command.onecmd('create User email="gui@hbtn.io"\
                                password="guipwd" first_name="Guillaume"\
                                last_name="Snow"')
            created_idd = mock_stdout.getvalue().strip()
            self.assertIn('State.{}'.format(created_idd), storage.all().keys())
            """


if __name__ == '__main__':
    unittest.main()
