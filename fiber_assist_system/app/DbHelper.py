# coding=utf-8
# import MySQLdb
import pymysql as MySQLdb
import time

# https://www.tuicool.com/articles/zUBFbi

class MysqlHelper(object):
    """
    no necessary to know about this class, it is just a db helper
    """
    error_code = ''     # MySQL error code

    _conn = None        # database connection
    _cur = None         # data cursor
    _use_dict = False   # if use: MySQLdb.cursors.DictCursor

    _TIMEOUT = 30       # default: 30 sec
    _timecount = 0

    def __init__(self, dbconfig):
        try:
            self._conn = MySQLdb.connect(
                host=dbconfig['host'],
                port=dbconfig['port'],
                user=dbconfig['user'],
                passwd=dbconfig['passwd'],
                db=dbconfig['db'],
                charset=dbconfig['charset']
            )
        except MySQLdb.Error as e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print (error_msg)

            # if not time out, try again，
            if self._timecount < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                self.__init__(dbconfig)
            else:
                raise Exception(error_msg)

        self._cur = self._conn.cursor(MySQLdb.cursors.DictCursor)

    def query(self, sql):
        """ execute SELECT statement """
        try:
            self._cur.execute("SET NAMES utf8")
            res = self._cur.execute(sql)
            # for field_desc in self._cur.description:
            #     print field_desc[0]
        except MySQLdb.Error as e:
            self.error_code = e.args[0]
            print("database error code: ", e.args[0], e.args[1])
            res = False
        return res

    def fetchAllRows(self):
        """ return result list """
        return self._cur.fetchall()

    def fetchOneRow(self):
        """ return one line of result and move cursor to next line.
            if cursor at the last line, return None
        """
        return self._cur.fetchone()

    def fetchManyRows(self, size=None):
        """ return multi-line result """
        return self._cur.fetchmany(size)

    def getRowCount(self):
        """ return number lines of the result """
        return self._cur.rowcount

    def commit(self):
        """ database commit operator """
        self._conn.commit()

    def close(self):
        """ close database connection """
        try:
            self._cur.close()
            self._conn.close()
        except: pass

if __name__ == '__main__':
    dbconf = {'host': '172.23.27.203', 'port': 3306, 'charset': 'utf8',
              'user': 'root', 'passwd': '123456', 'db': 'azkaban'}

    db = MysqlHelper(dbconf)
    sql = "select * from execution_jobs"
    db.query(sql)

    # fetch result list
    result = db.fetchAllRows()

    # iter row of result
    for row in result:
        # use k,v to get value
        print(row)

    db.close()



