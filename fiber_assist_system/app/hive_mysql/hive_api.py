# coding=utf-8
import app.hive_mysql.AzkabanMonitor as AzkabanMonitor
import pandas as pd
import app.hive_mysql.hive_properties as hive_properties
from app.hive_mysql import mysql_properties


def autoDeployProjectFlow(monitor,project_name,zip_file_path,cronExpr):
    monitor.autoDeployProjectFlow(project_name,zip_file_path,cronExpr)

def executeFlow(monitor,project,flow_name):
    monitor.executeFlow(project, flow_name)

def pauseFlowExecution(monitor,project_name,flow_name):
    exec_id=monitor.fetchFirstRunningExecutionId(project_name, flow_name)
    if exec_id:
        monitor.pauseFlowExecution(exec_id=exec_id)
    else:
        print(project_name + ' is not running!')


def cancelFlowExecution(monitor,project_name,flow_name):
    exec_id=monitor.fetchFirstRunningExecutionId(project_name, flow_name)
    if exec_id:
        monitor.cancelFlowExecution(project_name, flow_name, exec_id=exec_id)
    else:
        print(project_name + ' is stopped!')


def resumeFlowExecution(monitor,project_name,flow_name):
    exec_id=monitor.fetchFirstRunningExecutionId(project_name, flow_name)
    if exec_id:
        monitor.resumeFlowExecution(exec_id=exec_id)
    else:
        print('No Flow has been resumed')


def fetchExecutionJobLogs(monitor,project_name,flow_name,job_id_path,length):
    jobid=pd.read_table(job_id_path,header=None,sep=',')
    jobid=jobid.get(0)
    logs=[]
    for i in range(len(jobid)):
        temp=jobid[i].replace('.job','')
        exec_id=monitor.fetchExecutionsFlow(project_name=project_name, flow=flow_name, start=0, length=10)
        if exec_id:
            exec_id=exec_id['executions'][0]['execId']
            logs.append(monitor.fetchExecutionJobLogs(exec_id=exec_id, job_id=temp, length=length))
        else:
            logs.append('No project')
    return logs


def get_hive_properties():
    props = hive_properties.parse("E:\\PYProject\\tongding_projrct\\app\\hive_mysql\\hive_conf")
    print(props)
    monitor = AzkabanMonitor.AzkabanMonitor(props.get('base'), 'azkaban', 'azkaban',
                                            {'host': props.get('host'), 'port': int(props.get('port')),
                                             'charset': 'utf8', 'user': props.get('user'),
                                             'passwd': props.get('passwd'), 'db': props.get('db')}, 'INFO', 'file')
    return props,monitor


#一键部署
def hive_autoDeployProjectFlow():
    try:
        props, monitor = get_hive_properties()
        autoDeployProjectFlow(monitor, props.get('project_name'), props.get('zip_file_path'), props.get('cronExpr'))
    except Exception as e:
        print(e)

#运行
def hive_executeFlow():
    try:
        props, monitor = get_hive_properties()
        executeFlow(monitor, props.get('project_name'), props.get('flow_name'))
    except Exception as e:
        print(e)

#暂停
def hive_pauseFlowExecution():
    try:
        props, monitor = get_hive_properties()
        pauseFlowExecution(monitor, props.get('project_name'), props.get('flow_name'))
    except Exception as e:
        print(e)

#停止
def hive_cancelFlowExecution():
    try:
        props, monitor = get_hive_properties()
        cancelFlowExecution(monitor, props.get('project_name'), props.get('flow_name'))
    except Exception as e:
        print(e)

#暂停
def hive_resumeFlowExecution():
    try:
        props, monitor = get_hive_properties()
        resumeFlowExecution(monitor, props.get('project_name'), props.get('flow_name'))
    except Exception as e:
        print(e)

#显示日志
def hive_fetchExecutionJobLogs():
    try:
        props, monitor = get_hive_properties()
        logs=fetchExecutionJobLogs(monitor, props.get('project_name'), props.get('flow_name'), "E:\\PYProject\\tongding_projrct\\app\\hive_mysql\\job_id.txt",
                              length=1000)
    except Exception as e:
        logs =e
    return logs

if __name__ == '__main__':
    # ==================================== Hive API ====================================#
    # props =hive_properties.parse('./hive_conf')
    # monitor = AzkabanMonitor.AzkabanMonitor(props.get('base'), 'azkaban', 'azkaban', {'host': props.get('host'), 'port': int(props.get('port')), 'charset': 'utf8','user': props.get('user'), 'passwd': props.get('passwd'), 'db': props.get('db')}, 'DEBUG', 'file')
    # # ==================================== Azkaban API ====================================
    # # autoDeployProjectFlow(monitor,props.get('project_name'),props.get('zip_file_path'),props.get('cronExpr'))  ##一键部署
    # # executeFlow(monitor,props.get('project_name'),props.get('flow_name'))   ##运行
    # # pauseFlowExecution(monitor,props.get('project_name'),props.get('flow_name'))   ##暂停
    # # cancelFlowExecution(monitor,props.get('project_name'),props.get('flow_name'))   ##停止
    # # resumeFlowExecution(monitor,props.get('project_name'),props.get('flow_name'))   ##重启
    # logs=fetchExecutionJobLogs(monitor,props.get('project_name'),props.get('flow_name'),props.get('job_id'),length=1000)
    # print(logs['data'])
    #==================================== Mysql API ====================================#

    logs = hive_fetchExecutionJobLogs()
    for log in logs:
        print(log)




