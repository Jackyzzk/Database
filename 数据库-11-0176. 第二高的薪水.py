import pymysql


class Solution(object):
    """
编写一个 SQL 查询，获取 Employee 表中第二高的薪水（Salary） 。
+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
例如上述 Employee 表，SQL查询应该返回 200 作为第二高的薪水。如果不存在第二高的薪水，那么查询应返回 null。
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+
链接：https://leetcode-cn.com/problems/second-highest-salary
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
                "insert into Employee (Id, Salary) values ('2', '300')",
                "insert into Employee (Id, Salary) values ('3', '300')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def salary(self):
        # limit 语法
        # --------------------
        # SELECT * FROM tbl LIMIT 5,10;  # Retrieve rows 6-15
        # With two arguments, the first argument specifies the offset of the first row to return,
        # and the second specifies the maximum number of rows to return. The offset of the initial row is 0
        # select NULL 会返回 NULL 值而不是返回空
        # ----------------------------------------
        # if 语法
        # IF(expr1,expr2,expr3)
        # If expr1 is TRUE (expr1 <> 0 and expr1 <> NULL), IF() returns expr2. Otherwise, it returns expr3.
        # IFNULL(expr1,expr2)
        # If expr1 is not NULL, IFNULL() returns expr1; otherwise it returns expr2.
        # NULLIF(expr1,expr2)
        # Returns NULL if expr1 = expr2 is true, otherwise returns expr1.
        # This is the same as CASE WHEN expr1 = expr2 THEN NULL ELSE expr1 END.
        try:
            sql1 = """
                select
                    max(Salary) as SecondHighestSalary
                from
                    Employee
                where 
                    Salary not in 
                        (select 
                            max(Salary)
                        from 
                            Employee);
                """
            sql2 = """
                select
                    max(Salary) as SecondHighestSalary
                from
                    Employee as e1 left join
                        (select
                            max(Salary) as m
                        from 
                            Employee) as e2
                on
                    e1.Salary = e2.m
                where 
                    e2.m is NULL;
                """
            sql3 = """
                select
                    (select 
                        distinct Salary
                    from 
                        Employee
                    order by 
                        Salary DESC 
                    limit 
                        1, 1) as SecondHighestSalary;
                """  # select 后可以直接接上一个唯一的结果，即 一个只有一行一列的结果
            sql4 = """
                select
                    ifnull(
                        (select
                            distinct Salary
                        from
                            Employee
                        order by 
                            Salary DESC 
                        limit 
                            1, 1), NULL) as SecondHighestSalary;
                """
            self.cs.execute(sql4)
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

