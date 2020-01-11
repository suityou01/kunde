import unittest
from PIL import Image
from org import create_org, update_org, delete_org \
,read_org, add_new_person, remove_person, add_contact_route, update_contact_route \
, delete_contact_route, add_address, update_address, delete_address \
, add_document, update_document, delete_document, read_person, read_address \
, read_document, read_contact_route

class TestOrgMethods(unittest.TestCase):

    def test_create_org(self):
        id = create_org('Test Org','sysadmin')
        print('id = ' + str(id))
        self.assertTrue(id > 0)

    def test_update_org(self):
        id = update_org(2,'updated org','sysadmin')
        print(id)
        self.assertTrue(id == 2)
    
    def test_delete_org(self):
        ret = delete_org(2)
        print(ret)
        self.assertTrue(ret)
    
    def test_read_org(self):
        ret = read_org(2)
        print(ret[0][0])
        self.assertTrue(ret[0][0]=='Test Org')

    def test_add_new_person(self):
        ret = add_new_person(2,'Fred','Flintstone',1,'sysadmin')
        print(ret)
        self.assertTrue(ret>0)

    def test_remove_person(self):
        ret = remove_person(2,9,'Testing','sysadmin')
        self.assertTrue(ret)

    def test_read_person(self):
        ret = read_person(2, True)
        print(ret)

    def test_add_contact_route(self):
        ret = add_contact_route(2,'Test Contact Route', '123456789', 1,'sysadmin')
        print(ret)
        self.assertTrue(ret>0)

    def test_update_contact_route(self):
        ret = update_contact_route(1,'Updated Test Contact Route', '987654321','sysadmin')
        self.assertTrue(ret==True)

    def test_delete_contact_route(self):
        ret = delete_contact_route(1,'sysadmin')
        self.assertTrue(ret==True)

    def test_read_contact_route(self):
        ret = read_contact_route(1,True)
        print(ret)

    def test_add_address(self):
        ret = add_address(1,'20 Hart Hill Drive', '','Luton','Bedfordshire', 'LU20AX',234,1,'sysadmin')
        print(ret)
        self.assertTrue(ret>0)

    def test_read_address(self):
        ret = read_address(1)
        print(ret)
    
    def test_update_address(self):
        ret = update_address(5,'25 Hart Hill Drive', '','Luton','Bedfordshire', 'LU20AX',234,'sysadmin')
        self.assertTrue(ret)
    
    def test_read_org_from_zip(self):
        #ret = read_org(zip='LU2%',include_inactive=True)
        ret = read_org(name='The%',include_inactive=True)
        print(ret)

    def test_delete_address(self):  
        ret = delete_address(5,'sysadmin')
        print(ret)

    def test_add_document(self):
        img = Image.new( 'RGB', (255,255), "green") # Create a new green image
        ret = add_document(1,"Test document", img.tobytes(), 4,'sysadmin')
        print(ret)
        self.assertTrue(ret > 0)

    def test_update_document(self):
        img = Image.new( 'RGB', (500,500), "red") # Create a new red image
        ret = update_document(1,"Updated document", img.tobytes(),'sysadmin')
        print(ret)
        self.assertTrue(ret)

    def test_delete_document(self):
        ret = delete_document(1,'sysadmin')
        print(ret)
        self.assertTrue(ret)
    
    def test_read_document(self):
        ret = read_document(1,True)
        print(ret)

if __name__ == '__main__':
    unittest.main()