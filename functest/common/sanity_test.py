from jcsclient import client
from jcsclient import clilib
import unittest
import logging
import time
import utils
import sys

### Usage info
### Make sure you have sorced openrc and
### you have jcsclient installed before 
### starting this script

class SanityTest(unittest.TestCase):

    def __init__(self,*args, **kargs) : #access=None,secret=None,vpc_url = None, compute_url=None):
        super(SanityTest,self).__init__(*args, **kargs)
        self.jclient = client.Client()#access_key = access, secret_key = secret, vpc_url = vpc_url , compute_url = compute_url )

    @classmethod
    def setUpClass(self):

        LOG_FILENAME = 'sanity_test.log'
        logging.basicConfig(filename=LOG_FILENAME, 
                        level=logging.INFO,
                        )

        logging.info( "Calling setup")
        self.vpcId = None
        self.subnetId = None
        self.securityGroupId = None
        self.instanceId = None
        self.allocateAddressId = None
        self.associateAddressId = None
        self.routeTableId = None
        self.rtbAssocId = None

        logging.info('Starting sanity test')




    @classmethod
    def tearDownClass(self):
        logging.info( "Calling teardown")
        pass

    def test_create_vpc(self):
        resp = self.jclient.vpc.create_vpc(cidr_block='125.16.0.0/24')
        logging.info(resp)
        self.assertEqual(200, resp['status'])
        self.__class__.vpcId = resp['CreateVpcResponse']['vpc']['vpcId']


    def test_create_subnet(self):
        if self.__class__.vpcId:
            resp = self.jclient.vpc.create_subnet(vpc_id = self.vpcId, cidr_block='125.16.0.64/26')
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.subnetId = resp['CreateSubnetResponse']['subnet']['subnetId']
        else:
            self.fail('Vpc not created')    


    def test_create_security_group(self):
        if self.__class__.vpcId:
            resp = self.jclient.vpc.create_security_group(group_name='SanityTest', vpc_id=self.vpcId, description='Unit testcase group')
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.securityGroupId = resp['CreateSecurityGroupResponse']['groupId']
        else:
            self.fail('Vpc not created')



    def test_delete_subnet(self):
        if self.__class__.subnetId :
            time.sleep(5)
            resp = self.jclient.vpc.delete_subnet(subnet_id=self.subnetId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Subnet not created')

    def test_delete_security_group(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.delete_security_group(group_id= self.securityGroupId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else :
            self.fail('Security Group not created')

    def test_add_remove_group_rule(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.authorize_security_group_ingress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.authorize_security_group_ingress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logging.info(resp)
            self.assertEqual(200, resp['status'])

            resp = self.jclient.vpc.revoke_security_group_ingress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.revoke_security_group_ingress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logging.info(resp)
            self.assertEqual(200, resp['status'])




            resp = self.jclient.vpc.authorize_security_group_egress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.authorize_security_group_egress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logging.info(resp)
            self.assertEqual(200, resp['status'])

            resp = self.jclient.vpc.revoke_security_group_egress(group_id= self.securityGroupId, protocol='tcp', port='22', cidr = '10.0.0.0/24')
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.revoke_security_group_egress(group_id= self.securityGroupId, ip_permissions='[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/0"}, {"CidrIp": "20.0.0.0/0"}]}]')
            logging.info(resp)
            self.assertEqual(200, resp['status'])





        else :
            self.fail('Security Group not created')




    def test_delete_vpc(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.delete_vpc(vpc_id=self.__class__.vpcId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('VPC not created')


    def test_describe_vpcs(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.describe_vpcs(vpc_ids=self.__class__.vpcId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('VPC not created')


    def test_describe_subnets(self):
        if self.__class__.subnetId :
            resp = self.jclient.vpc.describe_subnets(subnet_ids=self.__class__.subnetId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Subnet not created')



    def test_describe_security_groups(self):
        if self.__class__.securityGroupId :
            resp = self.jclient.vpc.describe_security_groups(group_ids=self.__class__.securityGroupId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('SecurityGroup not created')

    def test_describe_vpc(self):
        if self.__class__.vpcId :
            resp = self.jclient.vpc.describe_vpcs(vpc_ids=self.__class__.vpcId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('VPC not created')



    def test_run_instance(self):
        images = self.jclient.compute.describe_images()['DescribeImagesResponse']['imagesSet']['item']
        for image in images:
            if image['name'] == "Ubuntu 14.04":
                imageId = image['imageId']
        resp = self.jclient.compute.run_instances(subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small', block_device_mappings="DeviceName=/dev/vda,DeleteOnTermination=true,VolumeSize=20")
        logging.info(resp)


        self.assertEqual(200, resp['status'])
        self.__class__.instanceId = resp['RunInstancesResponse']['instancesSet']['item']['instanceId']
    

        start_time = time.time()
        while True:
            resp = self.jclient.compute.describe_instances(instance_ids=self.__class__.instanceId)
            logging.info(resp)

            state = resp['DescribeInstancesResponse'][ 'instancesSet'][ 'item']
            state = resp['DescribeInstancesResponse'][ 'instancesSet'][ 'item'][ 'instanceState']

            if state =='running':
                #logger and logger.info(resp)
                break
            if (time.time() - start_time) >= 300:
                #logger and logger.error(resp)
                logging.error('Instance in pending state')
                self.fail('Instance stuck in pending state')

                break



    def test_terminate_instance(self):
        if self.__class__.instanceId :
            resp = self.jclient.compute.terminate_instances(instance_ids=self.__class__.instanceId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Instance not created')


    def test_create_route_table(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.create_route_table(vpc_id=self.__class__.vpcId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.routeTableId = resp['CreateRouteTableResponse']['routeTable']['routeTableId']
        else:
            self.fail('Instance not created')
 
    def test_add_route(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.create_route(instance_id=self.__class__.instanceId, route_table_id = self.__class__.routeTableId, destination_cidr_block = "10.0.0.0/24")
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Instance not created')


    def test_associate_route_table(self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.associate_route_table(route_table_id = self.__class__.routeTableId, subnet_id = self.__class__.subnetId )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.rtbAssocId = resp['AssociateRouteTableResponse']['associationId']
        else:
            self.fail('RTB not created')
        

    def test_describe_route_table(self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.describe_route_tables(route_table_ids = self.__class__.routeTableId )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('RTB not created')

    def test_disassociate_route_table (self):
        if self.__class__.rtbAssocId :
            resp = self.jclient.vpc.disassociate_route_table(association_id = self.__class__.rtbAssocId )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('RTB not created')


    def test_delete_route (self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.delete_route( route_table_id = self.__class__.routeTableId, destination_cidr_block = "10.0.0.0/24")
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('RTB not created')



    def test_delete_route_table (self):
        if self.__class__.routeTableId :
            resp = self.jclient.vpc.delete_route_table(route_table_id = self.__class__.routeTableId )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('RTB not created')


    def test_allocate_address(self):
        if self.__class__.instanceId :
            resp = self.jclient.vpc.allocate_address(domain='vpc')
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.allocateAddressId = resp['AllocateAddressResponse']['allocationId']
        else:
            self.fail('Instance not created')


    def test_associate_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId , instance_id = self.__class__.instanceId )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.associateAddressId = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address not allcoated')



    def test_describe_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.describe_addresses(allocation_ids = self.__class__.allocateAddressId )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Address not allcoated')




    def test_disassociate_address(self):
        if self.__class__.associateAddressId :
            resp = self.jclient.vpc.disassociate_address(association_id = self.__class__.associateAddressId )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Address not associated')



    def test_release_address(self):
        if self.__class__.allocateAddressId :
            resp = self.jclient.vpc.release_address(allocation_id= self.__class__.allocateAddressId)
            logging.info(resp)
            self.assertEqual(200, resp['status'])
        else:
            self.fail('Address not allcoated')


if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    test = unittest.TestSuite()
    test.addTest(SanityTest("test_create_vpc")) 
    test.addTest(SanityTest("test_describe_vpcs"))    
    test.addTest(SanityTest("test_create_subnet"))
    test.addTest(SanityTest("test_describe_subnets"))
    test.addTest(SanityTest("test_create_security_group"))
    test.addTest(SanityTest("test_add_remove_group_rule"))
    test.addTest(SanityTest("test_describe_security_groups"))
    test.addTest(SanityTest("test_run_instance"))
    test.addTest(SanityTest("test_create_route_table"))
    test.addTest(SanityTest("test_add_route"))
    test.addTest(SanityTest("test_delete_route"))
    test.addTest(SanityTest("test_associate_route_table"))
    test.addTest(SanityTest("test_describe_route_table"))
    test.addTest(SanityTest("test_allocate_address"))
    test.addTest(SanityTest("test_associate_address"))
    test.addTest(SanityTest("test_describe_address"))
    test.addTest(SanityTest("test_disassociate_address"))
    test.addTest(SanityTest("test_release_address"))
    test.addTest(SanityTest("test_disassociate_route_table"))
    test.addTest(SanityTest("test_delete_route_table"))
    test.addTest(SanityTest("test_terminate_instance"))
    test.addTest(SanityTest("test_delete_security_group"))
    test.addTest(SanityTest("test_delete_subnet"))
    test.addTest(SanityTest('test_delete_vpc'))
    ret = not unittest.TextTestRunner(verbosity=2).run(test).wasSuccessful()
    # ret = not runner.run(suite).wasSuccessful()
    sys.exit(ret)
