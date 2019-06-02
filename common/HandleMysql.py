"""
------------------------------------
@Time : 2019/5/30 11:36
@Auth : linux超
@File : HandleMysql.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import random
import string
import pymysql
from collections import Iterable

from common.ParseConfig import do_conf
# from common.RecordLog import log


class HandleMysql(object):
    def __init__(self):
        self._conn = self.__connect_mysql()
        self._cursor = None
        if self._conn:
            self._cursor = self._conn.cursor()
        else:
            raise ConnectionError('连接数据库失败!')

    def __connect_mysql(self):
        """连接数据库"""
        try:
            # log.info('start connecting MySQL...')
            self._conn = pymysql.connect(host=do_conf('MySQL', 'host'),
                                         user=do_conf('MySQL', 'user'),
                                         password=do_conf('MySQL', 'password'),
                                         db=do_conf('MySQL', 'db'),
                                         port=do_conf('MySQL', 'port'),
                                         charset=do_conf('MySQL', 'charset'),
                                         cursorclass=pymysql.cursors.DictCursor
                                         )
        except Exception as e:
            # log.error('connect MySQL failed\nDetails:{}'.format(e))
            self._conn = None
            return self._conn
        else:
            # log.info('connect MySQL success!')
            return self._conn

    def get_values(self, sql, args=None, is_all=False):
        if isinstance(args, Iterable) or args is None:
            if self._conn and self._cursor:
                self._cursor.execute(sql, args=args)
                # log.info('executing sql:{}'.format(sql))
                self._conn.commit()
                if isinstance(is_all, bool):
                    if is_all:
                        values = self._cursor.fetchall()
                    else:
                        values = self._cursor.fetchone()
                    # log.info('got values:{}'.format(values))
                    return values
                else:
                    # log.error('got values error: default parameter "{}" must be bool'.format(is_all))
                    raise TypeError('default parameter "{}" must be bool'.format(is_all))
            else:
                # log.error('due to the db connect failed, so get values error!')
                raise ConnectionError('due to the db connect failed, so get values error!')
        else:
            # log.error('got values error: default parameter args "{}" must be Iterable'.format(args))
            raise TypeError('default parameter args "{}" must be Iterable'.format(args))

    def __call__(self, sql, args=None, is_all=False):
        return self.get_values(sql, args=args, is_all=is_all)

    @staticmethod
    def phone_num():
        """随机生成3个角色的电话号码"""
        num_start = ['134', '135', '136', '137', '138',
                     '139', '150', '151', '152', '158',
                     '159', '157', '182', '187', '188',
                     '147', '130', '131', '132', '155',
                     '156', '185', '186', '133', '153',
                     '180', '189']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits, 8))
        phone_number = start + end
        return phone_number

    def get_phone(self):
        """判断生成的电话号码是否存在数据库中"""
        # db = HandleMysql()
        select_phone_sql = "select MobilePhone from member;"
        phone_number = self.get_values(sql=select_phone_sql, is_all=True)
        phone_list = []
        for phone_dic in phone_number:  # [{'MobilePhone': '18825046772'}, {'MobilePhone': '18825046772'}]
            phone_list.append(list(phone_dic.values())[0])
        while 1:
            phone = HandleMysql.phone_num()
            if phone not in phone_list:
                return phone

    def close(self):
        """自动关闭, 避免忘记关闭"""
        if self._cursor:
            self._cursor.close()
            # log.info('closing MySQL cursor...')
        if self._conn:
            self._conn.close()
            # log.info('closing MySQL connection...')


if __name__ == '__main__':
    sql_ = "SELECT MobilePhone FROM member limit %s;"
    mysql = HandleMysql()
    print(mysql.get_values(sql_, args=(1,), is_all=False))
    mysql.close()