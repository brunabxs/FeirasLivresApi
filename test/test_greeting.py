import unittest
from src.greeting import hello

class TestGreeting(unittest.TestCase):
    def test_hello_mustReturnHelloWorld(self):
        self.assertEqual(hello(), 'Hello World!')

if __name__ == '__main__':
    unittest.main()