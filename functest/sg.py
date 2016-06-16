#!/usr/bin/env python

from common import client
from common import utils
from common import vpc_manager
from common import subnet_manager
from common import security_group_manager
import unittest
import netaddr
import settings

class SecurityGroupCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
	self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.security_group_manager = security_group_manager.SecurityGroupManager(self.jclient)
        self.vpc_id = self.vpc_manager.create_vpc(cidr_block='172.0.0.0/24')

    def test_create_security_group(self):
        resp = self.jclient.vpc.create_security_group(group_name = 'Test1', group_description = 'ok', vpc_id = self.vpc_id)
        print resp
        self.assertEqual(200, resp['Status'])
        group_id1 = utils.get_item(('CreateSecurityGroupResponse','groupId'), resp)

        resp =  self.jclient.vpc.describe_security_groups(group_ids = group_id1) 
        print resp
        self.assertEqual(200, resp['Status'])

        resp =  self.jclient.vpc.delete_security_group(group_id = group_id1)
        print resp
        self.assertEqual(200, resp['Status'])

    def test_create_numeric_name_description_security_group(self) :

        resp = self.jclient.vpc.create_security_group(group_name = '1', group_description = 'ok', vpc_id = self.vpc_id)
        print resp
        self.assertEqual(200, resp['Status'])
        group_id2 = utils.get_item(('CreateSecurityGroupResponse','groupId'), resp)

        resp =  self.jclient.vpc.describe_security_groups(group_ids = group_id2)
        print resp
        self.assertEqual(200, resp['Status'])

        resp =  self.jclient.vpc.delete_security_group(group_id = group_id2)
        print resp
        self.assertEqual(200, resp['Status'])


        resp = self.jclient.vpc.create_security_group(group_name = 'Test1', group_description = '999', vpc_id = self.vpc_id)
        print resp
        self.assertEqual(200, resp['Status'])
        group_id3 = utils.get_item(('CreateSecurityGroupResponse','groupId'), resp)



        resp =  self.jclient.vpc.describe_security_groups(group_ids = group_id3)
        print resp
        self.assertEqual(200, resp['Status'])


        resp = self.jclient.vpc.create_security_group(group_name = '0x946', group_description = '010101', vpc_id = self.vpc_id)
        print resp
        self.assertEqual(200, resp['Status'])
        group_id4 = utils.get_item(('CreateSecurityGroupResponse','groupId'), resp)

        resp =  self.jclient.vpc.describe_security_groups(group_ids = group_id4)
        print resp
        self.assertEqual(200, resp['Status'])

        resp =  self.jclient.vpc.delete_security_group(group_id = group_id1)
        print resp
        self.assertEqual(200, resp['Status'])


if __name__ == '__main__':
    unittest.main()

