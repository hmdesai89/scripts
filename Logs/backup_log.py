import sys
from jcsclient import client
import put_logs as PS
import create_cross_account_policies as CP
from datetime import datetime , timedelta
import ConfigParser
import json
import getopt

def config_section_map(CONFIG, section):
    dict1 = {}
    options = CONFIG.options(section)
    for option in options:
        try:
            dict1[option] = CONFIG.get(section, option)
            if dict1[option] == -1 :
                print "Wrong Option"
        except:
            dict1[option]  = None
    return dict1



def initiate_client(secret):
    ##### Change this stuff and make it dynamic
    jclient = client.Client(access_key = secret['access_key'], secret_key = secret['secret_key'],
                            vpc_url=secret['vpc_url'],
                            compute_url=secret['compute_url'],
                            dss_url=secret['dss_url'],
                            iam_url=secret['iam_url'] )

    return jclient


def initiate_backup(config, secert, bucket_name):
    ''' Give full path of the config file.
        It should have time delt in days.
        Environment
     '''
    env = config['env']
    date = (datetime.now()-timedelta(days=int(config['time_delta']))).strftime('%Y%m%d')    
    jclient = initiate_client(secret) 
    PS.get_logs(date,env)
    PS.put_logs(date+'_'+env,bucket_name, jclient)
    




def policy_update(config,secret):
    ''' Give full path of the config file.
        It should have time delt in days.
        Environment
        bucket_name
        policy_name
        policy_action
        resources for that policy
        accounts which should have those policy attached
    '''

    jclient = initiate_client(secret)

 
    # if bucket name is changed


    bucket_name = config['bucket_name']
    PS.create_bucket(bucket_name,jclient)

 
    account_id =  CP.get_account_id(jclient)
    resources= []
    #if resource policy is changed
    for dict1 in config['resources']:
        dict1['account_id']= account_id
        dict1['resource']= 'Bucket:'+bucket_name
        resources.append(dict1)


    CP.create_resource_based_policy(config['policy_name'],[], [], jclient)
    CP.update_resource_based_policy(config['policy_name'],config['accounts'], config['actions'], jclient)
    CP.attach_policy_to_resource(config['policy_name'],resources,jclient)



if __name__=='__main__':


    CONFIG = ConfigParser.ConfigParser()
    CONFIG.read(sys.argv[1])
    logs = config_section_map(CONFIG, 'logs') 
    secret = config_section_map(CONFIG, 'secret')
    bucket = config_section_map(CONFIG, 'bucket')
    bucket['actions'] = bucket['actions'].split(',')
    bucket['accounts'] = bucket['accounts'].split(',')
    bucket['resources'] = [json.loads(resource) for resource in bucket['resources'].split(',')]




    for args in sys.argv:
        if args == '-u':
            policy_update(bucket, secret)
        if args == '-b' :
            initiate_backup(logs, secret, bucket['bucket_name'])
