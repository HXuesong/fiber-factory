# -*- coding: utf-8 -*-

from hdfs import *
import pandas as pd
import time
import datetime
import os

class HdfsClient(object):
    def __init__(self, conf=None):

        default_conf = {
            'server_url': 'http://172.23.27.203:50070',
            'cache_days': 1,
            'user': 'dm'
        }

        self.loc_conf = {
            'final_table_local_path': 'final_table.csv',
            'nearest_point_table_local_path': 'nearest_point_table.csv',
            'merged_point_table_local_path': 'merged_point_table.csv',

            'general_info_local_path': 'general_info.txt',

            'final_table_remote_path': '/user/dm/final_table.csv',
            'nearest_point_table_remote_path': '/user/dm/nearest_point_table.csv',
            'merged_point_table_remote_path': '/user/dm/merged_point_table.csv',
            'general_info_remote_path': '/user/dm/general_info.txt',
        }

        self._cache_conf = default_conf if conf is None else conf

        # hdfs client, establish a conn to hdfs server
        self._client = InsecureClient(
            url=self._cache_conf['server_url'],
            user=self._cache_conf['user']
        )

    @staticmethod
    def __get_file_create_time(file_path):
        create_time = os.path.getmtime(file_path)
        return create_time

    def __check_cache_time(self, local_path):
        now = time.time()
        print("create time: " + str(self.__get_file_create_time(local_path)))
        return (now - self.__get_file_create_time(local_path)) / 3600. > self._cache_conf['cache_days']

    def put_table(self, local_path, remote_path, force=True):
        """
        上传本地文件到HDFS
        :param local_path: 本地文件路径
        :param remote_path: HDFS文件路径
        :param force: 是否强制上传(无论文件是否存在)
        """
        table_name = local_path.split('/')[-1]
        file_lst = self._client.list('/'.join(remote_path.split('/')[:-1]))
        if table_name in file_lst:
            if force:
                self._client.delete(remote_path)
            else:
                print("table " + str(table_name) + " already exists, "
                                                   "If you want to force the file to be uploaded, set parameter force=True")
                return
        print("updating table " + table_name)
        self._client.upload(remote_path, local_path, n_threads=0)
        print("table " + table_name + " upload succeeded")
        return

    def _download_and_cache(self, remote_path, local_path):
        """
        # # 下载并缓存文件到本地, 本地文件过期则重新缓存
        # # :param remote_path:
        # # :param local_path:
        # # :return:
        # # """
        # if os.path.exists(local_path):
        #     if self.__check_cache_time(local_path):
        #         os.remove(local_path)
        #         self._client.download(remote_path, local_path, n_threads=0)
        # else:
        #     self._client.download(remote_path, local_path, n_threads=0)

    def get_table(self, local_path, remote_path):
        # """
        # 下载HDFS文件
        # :param local_path: 本地文件路径
        # :param remote_path: HDFS文件路径
        # """
        # self._download_and_cache(local_path=local_path, remote_path=remote_path)
        # print("loading table" + local_path.split('\\')[-1])
        final_table = pd.read_csv(local_path, encoding='gbk')
        return final_table

    def table_latest_info(self, table_name):
        """
        :param table_name: 'final', 'nearest_point', 'merged_point' are allowed
        :return: type of string timestamp with format "%Y-%m-%d %H:%M:%S"
        """
        remote_path = self.loc_conf[table_name + '_table_remote_path']
        state = self._client.status(remote_path)
        local_dt_time = datetime.datetime.fromtimestamp(state['modificationTime'] / 1000.0)
        local_dt_time = local_dt_time.strftime("%Y-%m-%d %H:%M:%S")
        return local_dt_time

    def view_table(self, table_name, n=10):
        """
        :param table_name: 'final', 'nearest_point', 'merged_point' are allowed
        :param n: get top n lines records
        :return top n records
        """
        local_path = self.loc_conf[table_name + '_table_local_path']
        remote_path = self.loc_conf[table_name + '_table_remote_path']
        table = self.get_table(local_path=local_path, remote_path=remote_path)
        return table.head(min(table.shape[0], n))

    def get_final_table_info(self):
        """ get final table information """
        local_path = self.loc_conf['final_table_local_path']
        remote_path = self.loc_conf['final_table_remote_path']
        final_table = self.get_table(local_path, remote_path)
        infos = {}
        infos['table_name'] = "final_table"
        infos["table_size"] = final_table.shape[0]
        infos["table_cols"] = final_table.shape[1]
        infos['update_time'] = self.table_latest_info("final")
        infos['num_bars'] = final_table["芯棒编码_密度测试"].drop_duplicates().shape[0]
        return infos

    @staticmethod
    def _parse_general_info(path):
        rows, cols = [], []
        column_names = []
        with open(path, 'r') as f:
            for line in f.readlines():
                if '------' in line:
                    if len(cols) > 0:
                        rows.append(cols[:])
                        cols = []
                        column_names = []
                else:
                    meta = line.split("#")
                    name, val = meta[0].strip(), meta[1].strip()
                    cols.append(val)
                    column_names.append(name)
        rows.append(cols[:])
        info = pd.DataFrame(rows, columns=column_names)
        info['UpdateTime'] = info['UpdateTime'].apply(lambda t: t.split('.')[0])
        return info

    def general_info(self, general_info_local_path, general_info_remote_path):
        """ get 11 hive tables information. """
        self._download_and_cache(local_path=general_info_local_path, remote_path=general_info_remote_path)
        info = self._parse_general_info(path=general_info_local_path)
        print("loading table " + general_info_local_path.split('\\')[-1])
        return info

    def refresh_info(self):
        print("=====================================")
        try:
            for k, v in self.loc_conf.items():
                if "local_path" in k and os.path.exists(v):
                    os.remove(v)
                    self._download_and_cache(
                        local_path=v, remote_path=self.loc_conf[k.replace("local", "remote")]
                    )
        except Exception:
            return False

        data = self.get_final_table_info()
        all_data = self.general_info(self.loc_conf['general_info_local_path'],self.loc_conf['general_info_remote_path'])
        return data,all_data

if __name__ == '__main__':


    hdfs_conf = {
        'server_url': 'http://172.23.27.203:50070',
        'cache_days': 1,
        'user': 'dm'
    }
    c = HdfsClient(conf=hdfs_conf)
    # print(c.table_latest_info('merged_point'))
    # c.view_table('final')
    # c.get_table(c.loc_conf['merged_point_table_local_path'], c.loc_conf['merged_point_table_remote_path'])
    # c.put_table(c.loc_conf['final_table_local_path'], c.loc_conf['final_table_remote_path'], force=True)
    # c.general_info(c.loc_conf['general_info_local_path'], c.loc_conf['general_info_remote_path'])
    data, alldata = c.refresh_info()
    print(data)
    # data = c.get_final_table_info()
    # all_data = c.general_info(c.loc_conf['general_info_local_path'], c.loc_conf['general_info_remote_path'])
    # print(data)
    # print(all_data)