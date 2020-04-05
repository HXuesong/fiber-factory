# coding=utf-8

from app.hive_mysql import mysql_properties, AzkabanMonitor


def autoDeployProjectFlow(monitor,project_name,zip_file_path,description):
    monitor.createProject(project_name, description)
    monitor.uploadProjectZip(project_name, zip_file_path)

def executeFlow(monitor,project_name,flow_name):
    exec_id=monitor.fetchFirstRunningExecutionId(project_name, flow_name)
    if exec_id:
        monitor.resumeFlowExecution(exec_id=exec_id)
    else:
        monitor.executeFlow(project_name, flow_name)

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


def fetchExecutionJobLogs(monitor,project_name,flow_name,job_id,length):
    exec_id=monitor.fetchExecutionsFlow(project_name=project_name, flow=flow_name, start=1, length=10)
    exec_id=exec_id['executions'][0]['execId']
    return monitor.fetchExecutionJobLogs(exec_id=exec_id, job_id=job_id, length=length)


def get_mysql_properties():
    props = mysql_properties.parse("./app/hive_mysql/mysql_conf")
    monitor = AzkabanMonitor.AzkabanMonitor(props.get('base'), 'azkaban', 'azkaban',
                                            {'host': props.get('host'), 'port': int(props.get('port')),
                                             'charset': 'utf8', 'user': props.get('user'),
                                             'passwd': props.get('passwd'), 'db': props.get('db')}, 'INFO', 'file')
    return props,monitor


def mysql_autoDeployProjectFlow():
    try:
        props, monitor = get_mysql_properties()
        autoDeployProjectFlow(monitor, props.get('project_name'), props.get('zip_file_path'),
                              props.get('auto_description'))
    except Exception as e:
        print(e)

def mysql_executeFlow():
    try:
        props, monitor = get_mysql_properties()
        executeFlow(monitor, props.get('project_name'), props.get('flow_name'))
    except Exception as e:
        print(e)

def mysql_cancelFlowExecution():
    try:
        props, monitor = get_mysql_properties()
        cancelFlowExecution(monitor, props.get('project_name'), props.get('flow_name'))
    except Exception as e:
        print(e)

def mysql_pauseFlowExecution():
    try:
        props, monitor = get_mysql_properties()
        pauseFlowExecution(monitor, props.get('project_name'), props.get('flow_name'))
    except Exception as e:
        print(e)


def mysql_fetchExecutionJobLogs():
    try:
        props, monitor = get_mysql_properties()
        logs = fetchExecutionJobLogs(monitor, props.get('project_name'), props.get('flow_name'), props.get('job_id'),
                                     length=100000)
    except Exception as e:
        logs = e
    return logs

if __name__ == '__main__':

    props =mysql_properties.parse('./mysql_conf')
    monitor = AzkabanMonitor.AzkabanMonitor(props.get('base'), 'azkaban', 'azkaban', {'host': props.get('host'), 'port': int(props.get('port')), 'charset': 'utf8','user': props.get('user'), 'passwd': props.get('passwd'), 'db': props.get('db')}, 'DEBUG', 'file')
    # ==================================== Azkaban API ====================================
    # autoDeployProjectFlow(monitor,props.get('project_name'),props.get('zip_file_path'),props.get('auto_description'))  ##一键部署
    executeFlow(monitor,props.get('project_name'),props.get('flow_name'))   ##运行  启动开始脚本和自动检测重启脚本
    # cancelFlowExecution(monitor,props.get('project_name'),props.get('flow_name'))   ##停止
    pauseFlowExecution(monitor,props.get('project_name'),props.get('flow_name'))   ##暂停
    logs=fetchExecutionJobLogs(monitor,props.get('project_name'),props.get('flow_name'),props.get('job_id'),length=10000)
    print(logs)
    # ==================================== Mysql API ====================================




