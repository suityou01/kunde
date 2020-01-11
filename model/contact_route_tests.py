import unittest
from contact_route import create_contact_route

class TestOrgMethods(unittest.TestCase):

    def test_create_or(self):
        create_contact_route('Main switchboard', '01234 555 666',999)
        self.assertEqual('foo'.upper(), 'FOO')

    
if __name__ == '__main__':
    unittest.main()