import pymysql


class Solution(object):
    """
给定一个 Weather 表，编写一个 SQL 查询，来查找与之前（昨天的）日期相比温度更高的所有日期的 Id。
+---------+------------------+------------------+
| Id(INT) | RecordDate(DATE) | Temperature(INT) |
+---------+------------------+------------------+
|       1 |       2015-01-01 |               10 |
|       2 |       2015-01-02 |               25 |
|       3 |       2015-01-03 |               20 |
|       4 |       2015-01-04 |               30 |
+---------+------------------+------------------+
例如，根据上述给定的 Weather 表格，返回如下 Id:
+----+
| Id |
+----+
|  2 |
|  4 |
+----+
链接：https://leetcode-cn.com/problems/rising-temperature
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Weather')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists Weather (Id int, RecordDate date, Temperature int)",
                "Truncate table Weather",
                "insert into Weather (Id, RecordDate, Temperature) values ('1', '2015-01-01', '10')",
                "insert into Weather (Id, RecordDate, Temperature) values ('2', '2015-01-02', '25')",
                "insert into Weather (Id, RecordDate, Temperature) values ('3', '2015-01-03', '20')",
                "insert into Weather (Id, RecordDate, Temperature) values ('4', '2015-01-04', '30')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def weather(self):
        # datediff 用来判断日期差值
        try:
            sql1 = """
                select
                    t1.Id
                from
                    Weather as t1, Weather as t2
                where
                    datediff(t1.RecordDate, t2.RecordDate) = 1 
                    and 
                    t1.Temperature > t2.Temperature
                """
            sql2 = """
                select
                    Id
                from
                    (select 
                        RecordDate as d, Temperature as t
                    from
                        Weather) as init,
                    Weather
                where
                    datediff(RecordDate, d) = 1 and Temperature > t
            """
            self.cs.execute(sql1)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            self.__del__()
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.weather()
    print(ret)


if __name__ == '__main__':
    main()

