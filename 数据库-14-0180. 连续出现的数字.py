import pymysql


class Solution(object):
    """
编写一个 SQL 查询，查找所有至少连续出现三次的数字。
+----+-----+
| Id | Num |
+----+-----+
| 1  |  1  |
| 2  |  1  |
| 3  |  1  |
| 4  |  2  |
| 5  |  1  |
| 6  |  2  |
| 7  |  2  |
+----+-----+
例如，给定上面的 Logs 表， 1 是唯一连续出现至少三次的数字。
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
链接：https://leetcode-cn.com/problems/consecutive-numbers
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Logs')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists Logs (Id int, Num int)",
                "Truncate table Logs",
                "insert into Logs (Id, Num) values ('1', '1')",
                "insert into Logs (Id, Num) values ('2', '1')",
                "insert into Logs (Id, Num) values ('3', '1')",
                "insert into Logs (Id, Num) values ('4', '2')",
                "insert into Logs (Id, Num) values ('5', '1')",
                "insert into Logs (Id, Num) values ('6', '2')",
                "insert into Logs (Id, Num) values ('7', '2')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def consecutive(self):
        try:
            sql1 = """
                select 
                    Num as ConsecutiveNums
                from
                    (select 
                        Num, max(
                        @cnt := 
                            if(@pre = Num, @cnt + 1, 
                                if(@pre := Num, 1, 1))) as k
                    from
                        Logs, (select @pre := NULL, @cnt := 1) as init
                    group by 
                        Num) as t1
                where
                    k > 2
                """
            sql2 = """
                select 
                    distinct Num as ConsecutiveNums
                from
                    (select 
                        Num, 
                        @cnt := 
                            if(@pre = Num, @cnt + 1, 
                                if(@pre := Num, 1, 1)) as k
                    from
                        Logs, (select @pre := NULL, @cnt := 1) as init) as t1
                where
                    k > 2
                """
            self.cs.execute(sql2)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            self.__del__()
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.consecutive()
    print(ret)


if __name__ == '__main__':
    main()

