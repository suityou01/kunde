import unittest
from person import create_person

class TestOrgMethods(unittest.TestCase):

    def test_create_person(self):
        id = create_person('Fred','Bloggs','sysadmin')
        self.assertTrue(id>0)

    
if __name__ == '__main__':
    unittest.main()