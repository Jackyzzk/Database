import pymysql


class Solution(object):
    """
某网站包含两个表，Customers 表和 Orders 表。编写一个 SQL 查询，找出所有从不订购任何东西的客户。
Customers 表：
+----+-------+
| Id | Name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+
Orders 表：
+----+------------+
| Id | CustomerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+
例如给定上述表格，你的查询应返回：
+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+
链接：https://leetcode-cn.com/problems/customers-who-never-order
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Customers')
        self.cs.execute('drop table Orders')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists Customers (Id int, Name varchar(255))",
                "Create table If Not Exists Orders (Id int, CustomerId int)",
                "Truncate table Customers",
                "insert into Customers (Id, Name) values ('1', 'Joe')",
                "insert into Customers (Id, Name) values ('2', 'Henry')",
                "insert into Customers (Id, Name) values ('3', 'Sam')",
                "insert into Customers (Id, Name) values ('4', 'Max')",
                "Truncate table Orders",
                "insert into Orders (Id, CustomerId) values ('1', '3')",
                "insert into Orders (Id, CustomerId) values ('2', '1')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def customers(self):
        try:
            sql1 = """
                select 
                    c.Name as Customers 
                from 
                    Customers as c left join Orders as o 
                on 
                    c.Id = o.CustomerId
                where 
                    o.CustomerId is NULL;
                """
            sql2 = """
                select 
                    Name as Customers
                from 
                    Customers
                where 
                    Id not in 
                        (select 
                            CustomerId as Id
                        from 
                            Orders);
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
    ret = test.customers()
    print(ret)


if __name__ == '__main__':
    main()

