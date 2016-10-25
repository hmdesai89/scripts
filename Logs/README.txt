This directory has scripts to take backup of logs on current production and staging setup.
Script backup_logs.py have general steps for taking backup.
Please make sure that you have latest VPC-tools and jcsclient installed from 
  http://10.140.192.133/JioCloudVPC

########## Example Usage


python2.7 Logs/backup_log.py Logs/sample_config.cfg -u -b
where 3rd argument is filepath.
-u wil create and update a bucket
-b will start a backup

## To DO

Make this implemenatation by puppet.


