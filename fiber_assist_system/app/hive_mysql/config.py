##### azkaban configuration
az_host = '10.5.7.1'
az_url = 'https://' + az_host + ':8443'
az_project = 'sql_to_hive'
az_flow_name = 'putInfo'

az_db_conf = {
    'host': az_host, 'port': 3306, 'charset': 'utf8',
    'user': 'root', 'passwd': 'root', 'db': 'azkaban'
}
##### hive connection configuration
master_host = '10.5.7.1'
active_namenode_host = '10.5.7.2'
active_namenode_hdfs_url = 'http://' + active_namenode_host + ':50070'

##### hdfs configuration
# hdfs client download file local cache base path and remote path
local_cache_base_path = r'G:\tongding_projrct\app\decisionpy'
remote_cache_base_path = '/user/final_table/'

# hdfs connection configuration - ha mode active namenode url
hdfs_conf = {
    'server_url': active_namenode_hdfs_url,
    'cache_hours': 5,
    'user': 'root'
}