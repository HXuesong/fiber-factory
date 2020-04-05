# coding=utf-8
import json
from urllib.parse import urljoin
import logging

import requests
import sys

from app.DbHelper import MysqlHelper
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AzkabanMonitor(object):
    """
    Args:
        | **base_url**: base url.
        | **username**: azkaban user name.
        | **password**: azkaban user password.
        | **dbConf**: database configuration, once you create `AzkabanMonitor` object, database
            will connection and hold till this object not used. This parameter is a type of `dict`
            you should contain key `host`, `port`, `user`, `passwd`, `db`, `charset`, if configuration
            is correct, mysql database will correct connected.
        | **log_level**: log level. `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`, default `INFO`.
        | **log_type**: log type. `file` or `std`.
    """
    def __init__(self, base_url, username, password, dbConf, log_level='INFO', log_type='file'):
        self.logger = self.__get_stdout_logger(__name__, log_level, log_type)
        self.logger.info("URL: {0}".format(base_url))
        self.__base_url = base_url
        self.__sess = requests.Session()
        self.authenticate(username, password)
        self.__db = MysqlHelper(dbConf)

    @property
    def base_url(self):
        return self.__base_url

    @staticmethod
    def __get_stdout_logger(logger_name, log_level_str, logger_type="file"):
        """ Get logger with stdout stream handler.
        :param logger_name: Logger identified name
        :type logger_name: str
        :param log_level_str: logger output level. (DEBUG, INFO, WARNING, ERROR)
        :type log_level_str: str
        :return: This class's root logger
        :rtype: logging.Logger
        """
        log_level = getattr(logging, log_level_str.upper())
        root_logger = logging.getLogger(logger_name)
        root_logger.setLevel(logging.DEBUG)
        if logger_type not in ['std', 'file']: logger_type='file'
        if logger_type=="std":
            logger_handler = logging.StreamHandler(sys.stdout)
        else:
            logger_handler = logging.FileHandler('./logging.log')
        logger_handler.setLevel(log_level)
        logger_handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)s [%(levelname)s] %(message)s"))
        root_logger.addHandler(logger_handler)
        return root_logger

    def authenticate(self, username, password):
        # http header
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'X-Requested-With': 'XMLHttpRequest'}

        # post data
        data = {'username': username, 'password': password, 'action': 'login'}

        # http://192.168.17.103:8443?action=login
        self.__sess = requests.Session()
        res = self.__sess.post(self.__base_url, headers=headers, data=data, verify=False)
        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error("Login Error")
            self.logger.error(res.json()['error'])
            raise self.AzkabanLoginError(res.json()['error'])
        else:
            self.logger.info("Success: Login %s with user %s", self.base_url, username)
            self.logger.debug(res.json())

    class AzkabanLoginError(Exception):
        """ Exception when login attempt failed. """
        pass

    class AjaxAPIError(Exception):
        """ Exception when requests is accepted but API call attempt failed. """
        pass

    # 0. Create a Project
    def createProject(self, project_name=None, desc=None):
        """The ajax API for creating a new project.

        Args:
            | **project_name**: project name.
            | **desc**: project description.

        Returns:
            True if create success.
        """
        api_url = urljoin(self.base_url, 'manager')
        data = {'name': project_name, 'description': desc, 'action': 'create'}
        res = self.__sess.post(api_url, data=data)

        if res.json()['status'] == 'error':
            if  "Project already exists" in res.json()['message']:
                self.logger.warning("Skip creating project %s because it already exists.", project_name)
                return False
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['message'])
        else:
            self.logger.info("Success: Create project - %s", project_name)
            self.logger.debug(res.json())
            return True

    # 1. Delete a Project
    def deleteProject(self, project_name):
        """
        The ajax API for deleting an existing project.

        Args:
            | **project_name**: project name.

        Returns:
            True if delete success.
        """
        api_url = urljoin(self.base_url, 'manager')
        params = {'project': project_name}
        res = self.__sess.get(api_url + '?delete=true', params=params)

        if res.status_code==200:
            self.logger.info("Success: Delete project - %s", project_name)
            return True
        return False

    # 2. Upload a Project Zip
    def uploadProjectZip(self, project_name, zip_path):
        """
        The ajax call to upload a project zip file.

        Args:
            | **project_name**: project name.
            | **zip_path**: zip file path.

        Returns:
            True if upload success.
        """
        api_url = urljoin(self.base_url, 'manager')
        data = {'project': project_name, 'ajax': 'upload'}
        files = {'file': ('jobs.zip', open(zip_path, 'rb'), 'application/x-zip-compressed')}
        res = self.__sess.post(api_url, data=data, files=files)

        if 'error' in res.json():
            self.logger.error(res.json())
            return False
        else:
            self.logger.info("Success: Upload project - %s", project_name)
            return True

    # 3. Fetch Flows of a Project
    def fetchProjectFlows(self, project_name):
        """
        Given a project name, this API call fetches all flow ids of that project.

        Args:
            | **project_name**: project name.

        Returns:
            json format response, A response sample:

            .. code-block:: javascript

               {
                  "project" : "test-azkaban",
                  "projectId" : 192,
                  "flows" : [ {
                    "flowId" : "test"
                  }, {
                    "flowId" : "test2"
                  } ]
                }

        Raises:
          AjaxAPIError: ajax api error.
        """
        api_url = urljoin(self.base_url, 'manager')
        params = {'project': project_name, 'ajax': 'fetchprojectflows'}
        res = self.__sess.get(api_url, params=params)

        if 'error' in res.json():
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['error'])
        else:
            self.logger.info("Success: Fetch project flow - %s", project_name)
            self.logger.debug(res.json())
            return res.json()

    # 4. Fetch Jobs of a Flow
    def fetchJobsFlow(self, project_name, flow):
        """
        For a given project and a flow id, this API call fetches all the jobs
        that belong to this flow. It also returns the corresponding graph structure
        of those jobs.

        Args:
          | **project_name**: project name.
          | **flow**: flow name.

        Returns:
            json format response, A response sample:

            .. code-block:: javascript

               {
                  "project" : "azkaban-test-project",
                  "nodes" : [ {
                    "id" : "test-final",
                    "type" : "command",
                    "in" : [ "test-job-3" ]
                  }, {
                    "id" : "test-job-start",
                    "type" : "java"
                  }],
                  "flow" : "test",
                  "projectId" : 192
                }

        Raises:
          AjaxAPIError: ajax api error.
        """
        api_url = urljoin(self.base_url, 'manager')
        params = {'project': project_name, 'flow': flow, 'ajax': 'fetchflowgraph'}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['error'])
        else:
            self.logger.info("Success: Fetch Jobs of a Flow - %s", flow)
            self.logger.debug(res.json())
            return res.json()

    # 5. Fetch Executions of a Flow
    def fetchExecutionsFlow(self, project_name, flow, start=0, length=3):
        """
        Given a project name, and a certain flow, this API call provides a list of
        corresponding executions. Those executions are sorted in descendent submit
        time order. Also parameters are expected to specify the start index and the
        length of the list. This is originally used to handle pagination.

        Args:
          | **project_name**: The project name to be fetched.
          | **flow**: The flow id to be fetched.
          | **start**: The start index(inclusive) of the returned list..
          | **length**: The max length of the returned list. For example, if the start
            index is 2, and the length is 10, then the returned list will include
            executions of indices: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11].

        Returns:
            json format response, A response sample:

            .. code-block:: javascript

               {
                  "executions" : [ {
                    "startTime" : 1407779928865,
                    "submitUser" : "1",
                    "status" : "FAILED",
                    "submitTime" : 1407779928829,
                    "execId" : 306,
                    "projectId" : 192,
                    "endTime" : 1407779950602,
                    "flowId" : "test"
                  }],
                  "total" : 16,
                  "project" : "azkaban-test-project",
                  "length" : 3,
                  "from" : 0,
                  "flow" : "test",
                  "projectId" : 192
                }

        Raises:
            AjaxAPIError: ajax api error.
        """
        api_url = urljoin(self.base_url, 'manager')
        params = {'project': project_name, 'flow': flow,
                  'ajax': 'fetchFlowExecutions', 'start': start, 'length': length}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['error'])
        else:
            self.logger.info("Success: Fetch Executions of a Flow - %s", flow)
            self.logger.debug(res.json())
            return res.json()

    # 6. Execute a Flow
    def executeFlow(self, project_name, flow):
        """
        This API executes a flow via an ajax call, supporting a rich selection
        of different options. Running an individual job can also be achieved
        via this API by disabling all other jobs in the same flow.

        Args:
            | **project_name**: The project name to be fetched.
            | **flow**: The flow id to be fetched.

        Returns:
            True if execute flow success.
        """
        api_url = urljoin(self.base_url, 'executor')
        params = {'project': project_name, 'flow': flow, 'ajax': 'executeFlow'}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            return False
        else:
            self.logger.info("Success: Execute Flow - %s", flow)
            self.logger.debug(res.json())
            return True

    # 7. Fetch Running Executions of a Flow
    def fetchRunningExecutionsFlow(self, project_name, flow):
        """
        Given a project name and a flow id, this API call fetches only executions
        that are currently running.

        Args:
            | **project_name**: The project name to be fetched.
            | **flow**: The flow id to be fetched.

        Returns:
            json format response, A response sample:

            .. code-block:: javascript

               {
                  "execIds": [301, 302]
                }

        Raises:
            AjaxAPIError: ajax api error.
        """
        api_url = urljoin(self.base_url, 'executor')
        params = {'project': project_name, 'flow': flow, 'ajax': 'getRunning'}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['error'])
        else:
            self.logger.info("Success: Fetch Running Executions of a Flow - %s", flow)
            self.logger.debug(res.json())
            return res.json()

    # 8. Cancel a Flow Execution
    def cancelFlowExecution(self, project_name, flow, exec_id):
        """
        Given an execution id, this API call cancels a running flow. If the
        flow is not running, it will return an error message.

        Args:
            | **project_name**: The project name to be fetched.
            | **flow**: The flow id to be fetched.

        Returns:
            True if execute flow success.
        """
        assert exec_id is not None
        api_url = urljoin(self.base_url, 'executor')
        params = {'project': project_name, 'flow': flow, 'ajax': 'cancelFlow', 'execid': exec_id}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            return False
        else:
            self.logger.info("Success: Cancel a Flow Execution - %s", flow)
            self.logger.debug(res.json())
            return True

    # 9. Flexible scheduling using Cron
    def flexibleScheduleUsingCron(self, project_name, flow, cronExpr='0 * * ? * *'):
        """
        This API call schedules a flow by a cron Expression. Cron is a UNIX tool that
        has been widely used for a long time, and we use Quartz library to parse cron
        Expression. All cron schedules follow the timezone defined in azkaban web server
        (the timezone ID is obtained by java.util.TimeZone.getDefault().getID()).

        Args:
            | **project_name**: The project name to be fetched.
            | **flow**: The flow id to be fetched.
            | **cronExpr**: A CRON expression is a string comprising 6 or 7 fields separated by
                white space that represents a set of times. In azkaban, we use Quartz Cron Format.

        Returns:
            An example success response:

            .. code-block:: javascript

               {
                  "message" : "PROJECT_NAME.FLOW_NAME scheduled.",
                  "scheduleId" : SCHEDULE_ID,
                  "status" : "success"
                }

            An example failure response:

            .. code-block:: javascript

               {
                  "message" : "Permission denied. Cannot execute FLOW_NAME",
                  "status" : "error"
                }

        Raises:
            AjaxAPIError: ajax api error.
        """
        api_url = urljoin(self.base_url, 'schedule')
        params = {'projectName': project_name, 'flow': flow,
                  'ajax': 'scheduleCronFlow', 'cronExpression': cronExpr}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['error'])
        else:
            self.logger.info("Success: Flexible scheduling using Cron - %s", flow)
            self.logger.debug(res.json())
            return res.json()

    # 10. Fetch a Schedule
    def fetchSchedule(self, project_id, flow_id):
        """
        Given a project id and a flow id, this API call fetches the schedule.

        Args:
            | **project_id**: The id of the project.
            | **flowId**: The name of the flow.

        Returns:
            json format response, A response sample:

            .. code-block:: javascript

               {
                  "schedule" : {
                    "cronExpression" : "0 * 9 ? * *",
                    "nextExecTime" : "2017-04-01 09:00:00",
                    "period" : "null",
                    "submitUser" : "azkaban",
                    "executionOptions" : {
                      "notifyOnFirstFailure" : false,
                      "notifyOnLastFailure" : false,
                      "failureEmails" : [ ],
                      "successEmails" : [ ],
                      "pipelineLevel" : null,
                      "queueLevel" : 0,
                      "concurrentOption" : "skip",
                      "mailCreator" : "default",
                      "memoryCheck" : true,
                      "flowParameters" : {
                      },
                      "failureAction" : "FINISH_CURRENTLY_RUNNING",
                      "failureEmailsOverridden" : false,
                      "successEmailsOverridden" : false,
                      "pipelineExecutionId" : null,
                      "disabledJobs" : [ ]
                    },
                    "scheduleId" : "3",
                    "firstSchedTime" : "2017-03-31 11:45:21"
                  }
                }

        Raises:
            AjaxAPIError: ajax api error.
        """
        api_url = urljoin(self.base_url, 'schedule')
        params = {'projectId': project_id, 'flowId': flow_id, 'ajax': 'fetchSchedule'}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['error'])
        else:
            self.logger.info("Success: Fetch a Schedule - %s", flow_id)
            self.logger.debug(res.json())
            return res.json()

    # 11. Unschedule a Flow
    def unscheduleFlow(self, schedule_id=None):
        """
        Given an execution id, this API call cancels a running flow. If the
        flow is not running, it will return an error message.

        Args:
            | **schedule_id**: The id of the schedule. You can find this in the
                Azkaban UI on the /schedule page.

        Returns:
            True if unschedule flow success.
        """
        api_url = urljoin(self.base_url, 'schedule')
        data = {'scheduleId': schedule_id, 'action': 'removeSched'}
        res = self.__sess.post(api_url, data=data)

        if 'error' in res.json()['status']:
            self.logger.error(res.json())
            return False
        else:
            self.logger.info("Success: Unschedule a Flow - %s", schedule_id)
            self.logger.debug(res.json())
            return True

    # 12. Pause a Flow Execution
    def pauseFlowExecution(self, exec_id):
        """
        Given an execution id, this API pauses a running flow. If an execution
        has already been paused, it will not return any error; if an execution
        is not running, it will return an error message.

        Args:
            | **exec_id**: The execution id.

        Returns:
            True if pause flow success.
        """
        assert exec_id is not None
        api_url = urljoin(self.base_url, 'executor')
        params = {'execid': exec_id, 'ajax': 'pauseFlow'}
        res = self.__sess.get(api_url, params=params)

        if 'error' in res.json():
            self.logger.error(res.json())
            return False
        else:
            self.logger.info("Success: Pause a Flow Execution - %s", exec_id)
            self.logger.debug(res.json())
            return True

    # 13. Resume a Flow Execution
    def resumeFlowExecution(self, exec_id):
        """
        Given an execution id, this API resumes a paused running flow. If an
        execution has already been resumed, it will not return any errors;
        if an execution is not runnning, it will return an error message.

        Args:
            | **exec_id**: The execution id.

        Returns:
            True if resume flow success.
        """
        assert exec_id is not None
        api_url = urljoin(self.base_url, 'executor')
        params = {'execid': exec_id, 'ajax': 'resumeFlow'}
        res = self.__sess.get(api_url, params=params)

        if 'error' in res.json():
            self.logger.error(res.json())
            return False
        else:
            self.logger.info("Success: Resume a Flow Execution - %s", exec_id)
            self.logger.debug(res.json())
            return True

    # 14. Fetch a Flow Execution
    def fetchFlowExecution(self, exec_id):
        """
        Given an execution id, this API call fetches all the detailed information
        of that execution, including a list of all the job executions.

        Args:
            | **exec_id**: The execution id to be fetched.

        Returns:
            json format response, A response sample:

            .. code-block:: javascript

               {
                  "attempt" : 0,
                  "submitUser" : "1",
                  "updateTime" : 1407779495095,
                  "status" : "FAILED",
                  "submitTime" : 1407779473318,
                  "projectId" : 192,
                  "flow" : "test",
                  "endTime" : 1407779495093,
                  "type" : null,
                  "nestedId" : "test",
                  "startTime" : 1407779473354,
                  "id" : "test",
                  "project" : "test-azkaban",
                  "nodes" : [ {
                    "attempt" : 0,
                    "startTime" : 1407779495077,
                    "id" : "test",
                    "updateTime" : 1407779495077,
                    "status" : "CANCELLED",
                    "nestedId" : "test",
                    "type" : "command",
                    "endTime" : 1407779495077,
                    "in" : [ "test-foo" ]
                  }],
                  "flowId" : "test",
                  "execid" : 304
                }

        Raises:
            AjaxAPIError: ajax api error.
        """
        assert exec_id is not None
        api_url = urljoin(self.base_url, 'executor')
        params = {'execid': exec_id, 'ajax': 'fetchexecflow'}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['error'])
        else:
            self.logger.info("Success: Fetch a Flow Execution - %s", exec_id)
            self.logger.debug(res.json())
            return res.json()

    # 15. Fetch Execution Job Logs
    def fetchExecutionJobLogs(self, exec_id, job_id, length=100):
        """
        Given an execution id and a job id, this API call fetches the correponding
        job logs. The log text can be quite large sometimes, so this API call also
        expects the parameters `offset` and `length` to be specified.

        Args:
            | **exec_id**: The execution id to be fetched.
            | **job_id**: The unique id for the job to be fetched.
            | **length**: The newest length of the log data.

        Returns:
            json format response, A response sample:

            .. code-block:: javascript

               {
                  "data" : "05-08-2014 16:53:02 PDT test-foobar INFO - Starting job test-foobar at 140728278",
                  "length" : 100,
                  "offset" : 0
                }

        Raises:
            AjaxAPIError: ajax api error.
        """
        assert exec_id is not None
        assert job_id is not None
        api_url = urljoin(self.base_url, 'executor')
        params = {'execid': exec_id, 'jobId': job_id,
                  'ajax': 'fetchExecJobLogs', 'offset': 0, 'length': int(1e9)}
        res = self.__sess.get(api_url, params=params)

        res.raise_for_status()
        if 'error' in res.json():
            self.logger.error(res.json())
            raise self.AjaxAPIError(res.json()['error'])
        else:
            self.logger.info("Success: Fetch Execution Job Logs - %s", (str(exec_id)+"-"+str(job_id)))
            self.logger.debug(res.json())
            org_json = res.json()
            data = org_json['data'].split('\n')
            lens = len(data)
            if lens==0: return res.json()
            truncLens = min(lens, length)
            truncData = '\n'.join(data[-truncLens: lens])
            org_json['data'] = truncData
            return org_json

    # 16. Auto deploy flow of project
    def autoDeployProjectFlow(self, project_name, default_zip_path, cronExpr):
        """
        Auto deploy flow of project, use default project name, description
        and use default schedule time interval.

        Args:
            | **default_zip_path**: default zip file path.
            | **cronExpr**: A CRON expression.

        Returns:
            True if deploy success.

        Raises:
            AjaxAPIError: ajax api error.
        """
        assert project_name is not None
        assert default_zip_path is not None
        assert cronExpr is not None

        desc = 'This is an auto deployed project, do not modify it.'

        # 0. prepare job
        if self.isActiveProject(project_name):
            is_scheduled, scheduleId = self.isScheduledProject(project_name)
            if is_scheduled: self.unscheduleFlow(scheduleId)
            self.deleteProject(project_name)
        self.createProject(project_name, desc)
        self.uploadProjectZip(project_name, default_zip_path)

        # 1. deploy job
        flows_info = self.fetchProjectFlows(project_name)
        flows = flows_info['flows']
        for flow in flows: # only have one flow
            flow_id = flow['flowId']
            self.flexibleScheduleUsingCron(project_name, flow_id, cronExpr)
        return True

    # 17. Project is scheduled
    def isScheduledProject(self, project_name):
        """
        Whether project is scheduled or not, only unscheduled project can be deleted.

        Args:
            | **project_name**: project.

        Returns:
            Return is a tuple: (is_scheduled, scheduleId), For first element True if project is
            scheduled now, if is_scheduled=False, scheduled=None.

        Raises:
            AjaxAPIError: ajax api error.
        """
        flows_info = self.fetchProjectFlows(project_name)
        project_id = flows_info['projectId']
        flows = flows_info['flows'] if "flows" in flows_info else None
        flow_id = ""
        for flow in flows:  # only have one flow
            flow_id = flow['flowId']
        schedule_info = self.fetchSchedule(project_id, flow_id)
        if len(schedule_info)==0:
            return False, None
        return True, schedule_info['schedule']['scheduleId']

    # 17. Fetch first running execution id.
    def fetchFirstRunningExecutionId(self, project_name, flow):
        """
        Fetch first running execution id for a given project name and flow id.
        For most of time, a project flow only have one execution id.

        Args:
            | **project_name**: project name.
            | **flow**: The flow id to be fetched.

        Returns:
            return execution id if flow is running, otherwise None
        """
        exec_json = self.fetchRunningExecutionsFlow(project_name, flow)
        if "execIds" in exec_json:
            exec_id = exec_json['execIds']
            if len(exec_id)>0:
                return exec_id[0]
        self.logger.error("Flow '" + str(flow) + "' is not running.")
        return None

    # 18. fetch project id.
    def fetchProjectId(self, project_name):
        """
        Fetch project id for a specific project.

        Args:
            | **project_name**: project name.

        Returns:
            project id
        """
        project_json = self.fetchProjectFlows(project_name)
        project_id = project_json['projectId']
        return project_id

    # ============================= Mysql API =============================
    def isActiveProject(self, project_name='autoProject'):
        """
        Is an active azkaban project?

        Args:
            | **project_name**: project name

        Returns:
            True if it is an active project
        """
        sql = "select name from projects where active=1"
        self.__db.query(sql)
        res = self.__db.fetchAllRows()
        for row in res:
            if project_name==row['name']: return True
        return False

    def fetchActiveFlows(self):
        """
        Fetch running flows in azkaban.

        Returns:
            json format response, A response sample:

            .. code-block:: javascript

               [{
                  "data" : "05-08-2014 16:53:02 PDT test-foobar INFO - Starting job test-foobar at 140728278",
                  "length" : 100,
                  "offset" : 0
                }]

        """
        sql = "select * from active_executing_flows"
        self.__db.query(sql)
        res = self.__db.fetchAllRows()
        # 对行进行循环
        active_flows = []
        for row in res:
            flow_info = self.fetchFlowExecution(row['exec_id'])
            active_flows.append(flow_info)
        if len(active_flows)==0:
            self.logger.info("no active flows")
        return json.dumps(active_flows)
        # 18. restart project

    def restartProject(self, is_first=False):
        """
        restart a project.

        Args:
            | **project_name**: project name.
            | **mode**: is_first=True if first call this method.

        Returns:
            True if the restart project finished.
        """
        res = self.fetchRunningExecutionsFlow("sql_to_hive", "putInfo")
        # project is running now, do nothing.
        if res.get('execIds') is not None:
            if is_first:  # just for clear
                return False  # waiting for finished
            else:
                return False  # waiting for finished
        # project is not running, restart it
        else:
            if is_first:
                self.executeFlow("sql_to_hive", "putInfo")
            else:
                return True

    def __del__(self):
        print("release mysql db resource")
        self.__db.close()

if __name__ == '__main__':

    dbConf = {'host': '172.23.27.203', 'port': 3306, 'charset': 'utf8',
              'user': 'root', 'passwd': '123456', 'db': 'azkaban'}

    base = 'https://172.23.27.203:8443'

    project = 'sql_to_hive'
    flow_name = 'putInfo'
    # project = 'autoProject'
    # flow_name = 'ping'

    description = 'azkaban ajax create project api test'
    zip_file_path = 'C:\\Users\\mdu\\Desktop\\az_upload_api1.zip'
    default_path = 'C:\\Users\\mdu\\Desktop\\autoProject.zip'
    default_cronExpr = '0 * * ? * *'

    monitor = AzkabanMonitor(base, 'azkaban', 'azkaban', dbConf, 'INFO', 'file')

    # ==================================== Azkaban API ====================================
    # monitor.createProject(project, description)
    # monitor.deleteProject(project)
    # monitor.uploadProjectZip(project, zip_file_path)
    # flowJson = monitor.fetchProjectFlows(project)
    # monitor.fetchJobsFlow(project, flow_name)
    # monitor.fetchExecutionsFlow(project, flow_name, start=1, length=4)
    # monitor.executeFlow(project, flow_name)
    # monitor.fetchRunningExecutionsFlow(project, flow_name)
    # monitor.cancelFlowExecution(project, flow_name, exec_id=monitor.fetchFirstRunningExecutionId(project, flow_name))
    # monitor.flexibleScheduleUsingCron(project, flow_name)                           # 执行定期调度
    # monitor.fetchSchedule(project_id=flowJson['projectId'], flow_id='hello2')       # 获取定期调度信息
    # monitor.unscheduleFlow(schedule_id=13)                                          # 取消定期调度
    # monitor.pauseFlowExecution(exec_id=700)
    # monitor.resumeFlowExecution(exec_id=7)
    # monitor.fetchFlowExecution(exec_id=128)
    # logs = monitor.fetchExecutionJobLogs(exec_id=1670, job_id='run_dataimport', length=100000)
    # data = logs['data']
    # print(data)
    # res = monitor.autoDeployProjectFlow('autoProject' , default_path, default_cronExpr)
    # res = monitor.isScheduledProject('jzj_api_test')
    # monitor.fetchFirstRunningExecutionId(project, flow_name)
    # res = monitor.fetchProjectId(project)
    # ==================================== Mysql API ====================================
    # res = monitor.isActiveProject("ss")
    # monitor.fetchActiveFlows()

    # monitor.restartProject(is_first=True)

    res = monitor.restartProject(is_first=False)
    print(res)