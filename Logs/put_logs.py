from jcsclient import client
from datetime import datetime
import sys
import os
from vpctools import vpc_functions as VF
import logging
### Usage info
### This file is helpful in gathering log files from all nodes in given environment
### This script expects bucket is already created
### And resource based policy is already in place.

LOG_FILENAME = 'log_test.log'
logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.DEBUG,
                        )


def get_logs(date, env):
    if not os.path.exists(date+'_'+env):
        os.makedirs(date+'_'+env)
    VF.Controlgetlogs(env, 'all', date+'_'+env, None, None, date)
    VF.EC2getlogs(env, 'all', date+'_'+env, None, None, date)

def put_logs(directory,bucket, jclient):
    for f in os.listdir(directory):
        logging.info( jclient.dss.put_object(['put-object','--bucket', bucket
                                              ,'--key', 'test/'+f
                                              ,'--body', directory+'/'+f]))

    logging.info( jclient.dss.list_objects(['list-objects','--bucket',bucket]))

def create_bucket(bucket, jclient):
    logging.info(jclient.dss.create_bucket(['create-bucket','--bucket', bucket]))
 
if __name__ == '__main__':
    date = '20161010'
    env = 'stag'
    bucket = 'log'
    get_logs(date,env)
    put_logs(date,bucket,jclient)    
