import unittest

from src.greeter import format_greeting, get_project_name


class GreeterTests(unittest.TestCase):
    def test_format_greeting(self):
        self.assertEqual(format_greeting("GitHub"), "Hello, GitHub!")

    def test_format_greeting_custom_message(self):
        self.assertEqual(format_greeting("Actions", greeting="Welcome"), "Welcome, Actions!")

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            format_greeting("   ")

    def test_project_name(self):
        self.assertEqual(get_project_name(), "github-actions-showcase")


if __name__ == "__main__":
    unittest.main()
