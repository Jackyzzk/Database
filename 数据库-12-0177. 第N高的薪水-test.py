import pymysql


class Solution(object):
    """
编写一个 SQL 查询，获取 Employee 表中第 n 高的薪水（Salary）。
+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
例如上述 Employee 表，n = 2 时，应返回第二高的薪水 200。如果不存在第 n 高的薪水，那么查询应返回 null。
+------------------------+
| getNthHighestSalary(2) |
+------------------------+
| 200                    |
+------------------------+
链接：https://leetcode-cn.com/problems/nth-highest-salary
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Employee')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists Employee (Id int, Salary int)",
                "Truncate table Employee",
                "insert into Employee (Id, Salary) values ('1', '100')",
                "insert into Employee (Id, Salary) values ('2', '200')",
                "insert into Employee (Id, Salary) values ('3', '300')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def salary(self):
        # create function 函数名([参数列表]) returns 数据类型
        # begin
        #  sql语句;
        #  return 值;
        # end;
        try:
            sql1 = """
                select 
                    ifnull(
                        (select
                            distinct Salary
                        from
                            Employee
                        order by
                            Salary DESC
                        limit 
                            %s, 1), NULL) as getNthHighestSalary;
                """
            self.cs.execute(sql1, 2 - 1)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            self.__del__()
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.salary()
    print(ret)


if __name__ == '__main__':
    main()

