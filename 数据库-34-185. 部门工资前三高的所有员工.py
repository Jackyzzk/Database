import pymysql


class Solution(object):
    """
Employee 表包含所有员工信息，每个员工有其对应的工号 Id，姓名 Name，工资 Salary 和部门编号 DepartmentId 。
+----+-------+--------+--------------+
| Id | Name  | Salary | DepartmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 85000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
| 7  | Will  | 70000  | 1            |
+----+-------+--------+--------------+
Department 表包含公司所有部门的信息。
+----+----------+
| Id | Name     |
+----+----------+
| 1  | IT       |
| 2  | Sales    |
+----+----------+
编写一个 SQL 查询，找出每个部门获得前三高工资的所有员工。例如，根据上述给定的表，查询结果应返回：
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| IT         | Randy    | 85000  |
| IT         | Joe      | 85000  |
| IT         | Will     | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+
解释：
IT 部门中，Max 获得了最高的工资，Randy 和 Joe 都拿到了第二高的工资，Will 的工资排第三。
销售部门（Sales）只有两名员工，Henry 的工资最高，Sam 的工资排第二。
链接：https://leetcode-cn.com/problems/department-top-three-salaries
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
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('1', 'Joe', '85000', '1')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('2', 'Henry', '80000', '2')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('3', 'Sam', '60000', '2')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('4', 'Max', '90000', '1')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('5', 'Janet', '69000', '1')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('6', 'Randy', '85000', '1')",
                "insert into Employee (Id, Name, Salary, DepartmentId) values ('7', 'Will', '70000', '1')",
                "Truncate table Department",
                "insert into Department (Id, Name) values ('1', 'IT')",
                "insert into Department (Id, Name) values ('2', 'Sales')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def employee(self):
        # CAST()函数将这个值转换为decimal类型，需要首先定义decimal值的精度与小数位数。
        # 精度是总的数字位数，包括小数点左边和右边位数的总和。而小数位数是小数点右边的位数。
        # AVG 函数返回数值列的平均值。NULL 值不包括在计算中。它会自动计算总数
        # sql 语句中不能使用连续等于的判断：
        # 系统会先第一个等号语句，（其实是个布尔表达式）得到的结果是1或者0，然后再用0或者1去跟第二个对比得到最终的结果
        try:
            sql1 = """
                select
                    Name, Salary, DepartmentId, 
                    @rank := if(DepartmentId != @pre_Id, 1, if(Salary != @pre_salary, @rank + 1, @rank)), 
                    @pre_salary := Salary, 
                    @pre_Id := DepartmentId
                from
                    Employee, (select @rank := 0, @pre_salary := -1, @pre_Id := -1) as init
                order by
                    DepartmentId, Salary DESC
            """
            sql2 = """
                select
                    d.Name as Department, e.Name as Employee, e.Salary
                from
                    Department as d
                        inner join
                            (select
                                Name, Salary, DepartmentId, 
                                @rank := if(DepartmentId != @pre_Id, 1, 
                                            if(Salary != @pre_salary, @rank + 1, @rank)) as r, 
                                @pre_salary := Salary, 
                                @pre_Id := DepartmentId
                            from
                                Employee, (select @rank := 0, @pre_salary := -1, @pre_Id := -1) as init
                            order by
                                DepartmentId, Salary DESC) as e
                        on
                            e.DepartmentId = d.Id
                where
                    e.r < 4
            """
            # 是不是select了变量的时候，存储的是表达式，最后输出的时候再运算？
            # 不然怎么解释最后的 order by 可以造成正确的 @rank值
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
    ret = test.employee()
    print(ret)


if __name__ == '__main__':
    main()


