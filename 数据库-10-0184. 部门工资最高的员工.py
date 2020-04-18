import pymysql


class Solution(object):
    """
Employee 表包含所有员工信息，每个员工有其对应的 Id, salary 和 department Id。
+----+-------+--------+--------------+
| Id | Name  | Salary | DepartmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 70000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
+----+-------+--------+--------------+
Department 表包含公司所有部门的信息。
+----+----------+
| Id | Name     |
+----+----------+
| 1  | IT       |
| 2  | Sales    |
+----+----------+
编写一个 SQL 查询，找出每个部门工资最高的员工。例如，根据上述给定的表格，
Max 在 IT 部门有最高工资，Henry 在 Sales 部门有最高工资。
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| Sales      | Henry    | 80000  |
+------------+----------+--------+
链接：https://leetcode-cn.com/problems/department-highest-salary
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Employee')
        self.cs.execute('drop table Department')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists Employee (Id int, Name varchar(255), Salary int, DepartmentId int)",
                "Create table If Not Exists Department (Id int, Name varchar(255))",
                "Truncate table Employee",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('1', 'Joe', '70000', '1')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('2', 'Jim', '90000', '1')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('3', 'Henry', '80000', '2')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('4', 'Sam', '60000', '2')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('5', 'Max', '90000', '1')",
                "Truncate table Department",
                "insert into Department (Id, Name) values ('1', 'IT')",
                "insert into Department (Id, Name) values ('2', 'Sales')",
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def salary(self):
        try:
            sql1 = """
                select 
                    d.Name as Department, e.Name as Employee, e.Salary
                from 
                    Department as d inner join Employee as e 
                on 
                    d.Id = e.DepartmentId
                where 
                    (e.DepartmentId, e.Salary) in 
                        (select 
                            DepartmentId, max(Salary)
                        from 
                            Employee
                        group by 
                            DepartmentId);
                """  # 可以元组 in
            sql2 = """
                select 
                    DepartmentId, max(Salary)
                from 
                    Employee
                group by 
                    DepartmentId
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
    ret = test.salary()
    print(ret)


if __name__ == '__main__':
    main()

