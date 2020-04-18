import pymysql


class Solution(object):
    """
Employee 表包含所有员工，他们的经理也属于员工。每个员工都有一个 Id，此外还有一列对应员工的经理的 Id。
+----+-------+--------+-----------+
| Id | Name  | Salary | ManagerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | NULL      |
| 4  | Max   | 90000  | NULL      |
+----+-------+--------+-----------+
给定 Employee 表，编写一个 SQL 查询，该查询可以获取收入超过他们经理的员工的姓名。
在上面的表格中，Joe 是唯一一个收入超过他的经理的员工。
+----------+
| Employee |
+----------+
| Joe      |
+----------+
链接：https://leetcode-cn.com/problems/employees-earning-more-than-their-managers
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
                "Create table If Not Exists Employee (Id int, Name varchar(255), Salary int, ManagerId int)",
                "Truncate table Employee",
                "insert into Employee (Id, Name, Salary, ManagerId) values ('1', 'Joe', '70000', '3')",
                "insert into Employee (Id, Name, Salary, ManagerId) values ('2', 'Henry', '80000', '4')",
                "insert into Employee (Id, Name, Salary, ManagerId) values ('3', 'Sam', '60000', NULL)",
                "insert into Employee (Id, Name, Salary, ManagerId) values ('4', 'Max', '90000', NULL)"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def employees(self):
        # left join 结构：
        # SELECT left_tbl. *
        # FROM left_tbl LEFT JOIN right_tbl
        # ON left_tbl.id = right_tbl.id
        # WHERE right_tbl.id IS NULL;
        # -------------------------------------
        # If there is no matching row for the right table in the ON or USING part in a LEFT JOIN,
        # a row with all columns set to NULL is used for the right table.
        # You can use this fact to find rows in a table that have no counterpart in another table
        # This example finds all rows in left_tbl with an id value that is not present in right_tbl
        # (that is, all rows in left_tbl with no corresponding row in right_tbl)
        # https://dev.mysql.com/doc/refman/5.7/en/join.html

        try:
            sql1 = """
                select 
                    e.Name as Employee
                from 
                    Employee as e left join Employee as m 
                on 
                    e.ManagerId = m.Id
                where 
                    e.Salary > m.Salary;
                """
            sql2 = """
                select 
                    e.Name as Employee
                from 
                    Employee as e inner join (select distinct Id, Salary from Employee) as m 
                on 
                    e.ManagerId = m.Id
                where 
                    e.Salary > m.Salary;
                """  # 160 ms 100%  inner join 会自动过滤掉 NULL
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
    ret = test.employees()
    print(ret)


if __name__ == '__main__':
    main()

