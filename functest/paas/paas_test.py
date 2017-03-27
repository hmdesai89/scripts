from jcsclient import client
from jcsclient import clilib
from client_v2_jcs.jcs_neutron import create_neutron_req as NR

import unittest
import logging
### Usage info
### Make sure you have sorced openrc and
### you have jcsclient installed before 
### starting this script
#   Test Cases
#   1. Create a PAAS port
#   2. List PAAS port - paas account
#   3. List PAAS port - customer account
#   4. Update PAAS port - customer account
#   5. Update PAAS port - paas account
#   6. Create a cross account port - non paas account
#   7. Delete a paas port - paas account
#   8. Delete a paas port - customer account
#   9. List ports - paas account

class PaasTest(unittest.TestCase):

    def __init__(self,*args, **kargs) : #access=None,secret=None,vpc_url = None, compute_url=None):
        super(PaasTest,self).__init__(*args, **kargs)
        self.jclient = client.Client()#access_key = access, secret_key = secret, vpc_url = vpc_url , compute_url = compute_url )

    @classmethod
    def setUpClass(self):


        access = 'SET MANUALLY'
        secret = SET MANUALLY
        vpc_url = SET MANUALLY
        compute_url = SET MANUALLY

        access2 = SET MANUALLY 
        secret2 = SET MANUALLY 

        access_paas = SET MANUALLY
        secret_paas = SET MANUALLY



        #self.jclient1 = client.Client(access_key = access, secret_key = secret, vpc_url = vpc_url , compute_url = compute_url )
	self.nc1 = NR.NeutronClient(access , secret) 

        self.jclient2 = client.Client(access_key = access2, secret_key = secret2, vpc_url = vpc_url , compute_url = compute_url )
        self.nc2 = NR.NeutronClient(access2 , secret2)

	#self.jclient_paas = client.Client(access_key = access_paas, secret_key = secret_paas, vpc_url = vpc_url , compute_url = compute_url )
	self.nc_paas = NR.NeutronClient(access_paas , secret_paas)

 
        LOG_FILENAME = 'paas_test.log'
        logging.basicConfig(filename=LOG_FILENAME, 
                        level=logging.INFO,
                        )

        logging.info( "Calling setup")


        logging.info(self.nc_paas.list_ports())

        logging.info(self.nc_paas.list_networks())

        resp = self.jclient2.vpc.create_vpc(cidr_block='193.169.0.0/24')
        logging.info(resp)

        self.vpcId = resp['CreateVpcResponse']['vpc']['vpcId']

        if self.vpcId:
            resp = self.jclient2.vpc.create_subnet(vpc_id = self.vpcId, cidr_block='193.169.0.64/26')
            logging.info(resp)
            self.subnetId = resp['CreateSubnetResponse']['subnet']['subnetId']
        else:
            self.fail('Vpc not created')

        _filter = {'type' : 'name', 'value': self.subnetId }

        
        self.paas_port_id = ''
        self.customer_net = self.nc2.list_networks(_filter)['data']['networks'][0]['id']
        logging.info('Customers network is '+self.customer_net) 


    def test_create_cross_port_paas_account(self):
        resp = self.nc_paas.create_port(network_id=self.customer_net, name = 'unit_test_paas')
        logging.info(resp)
        self.assertEqual(201, resp['status'])
        self.__class__.paas_port_id = resp['data']['port']['id']


    def test_create_cross_port_customer_account(self):
        resp = self.nc1.create_port(network_id=self.customer_net, name = 'unit _test_paas')
        logging.info(resp)
        self.assertEqual(403, resp['status'])

    def test_list_cross_port_paas_account(self):
        resp = self.nc_paas.list_port(port_id=self.paas_port_id)
        logging.info(resp)
        self.assertEqual(200, resp['status'])


    def test_list_cross_port_customer_account(self):
        resp = self.nc1.list_port(port_id=self.paas_port_id)
        logging.info(resp) 
        self.assertEqual(404, resp['status'])


    def test_delete_cross_port_paas_account(self):
        resp = self.nc_paas.delete_port(self.paas_port_id)
        logging.info(resp)
        self.assertEqual(204, resp['status'])


    def test_update_cross_port_paas_account(self):
        resp = self.nc_paas.update_port(port_id=self.paas_port_id, name = 'test_')
        logging.info(resp)
        self.assertEqual(200, resp['status'])

    def test_list_ports_paas_account(self):
        resp = self.nc_paas.list_ports()
        logging.info(resp)
        self.assertEqual(200, resp['status'])



    @classmethod
    def tearDownClass(self):
        logging.info( "Calling teardown")

        if self.subnetId :
            resp = self.jclient2.vpc.delete_subnet(subnet_id=self.subnetId)
            logging.info(resp)
        else:
            self.fail('Subnet not created')

        if self.vpcId :
            resp = self.jclient2.vpc.delete_vpc(vpc_id=self.vpcId)
            logging.info(resp)
        else:
            self.fail('VPC not created')


if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    test = unittest.TestSuite()
    test.addTest(PaasTest("test_create_cross_port_paas_account"))
    test.addTest(PaasTest("test_create_cross_port_customer_account"))    
    test.addTest(PaasTest("test_list_cross_port_paas_account"))
    test.addTest(PaasTest("test_list_cross_port_customer_account"))
    test.addTest(PaasTest("test_update_cross_port_paas_account"))
    test.addTest(PaasTest("test_delete_cross_port_paas_account"))

    unittest.TextTestRunner(verbosity=2).run(test)
