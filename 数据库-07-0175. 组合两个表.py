import pymysql


class Solution(object):
    """
表1: Person
+-------------+---------+
| 列名         | 类型    |
+-------------+---------+
| PersonId    | int     |
| FirstName   | varchar |
| LastName    | varchar |
+-------------+---------+
PersonId 是上表主键
表2: Address
+-------------+---------+
| 列名         | 类型    |
+-------------+---------+
| AddressId   | int     |
| PersonId    | int     |
| City        | varchar |
| State       | varchar |
+-------------+---------+
AddressId 是上表主键
编写一个 SQL 查询，满足条件：无论 person 是否有地址信息，都需要基于上述两表提供 person 的以下信息：
FirstName, LastName, City, State
链接：https://leetcode-cn.com/problems/combine-two-tables
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Person')
        self.cs.execute('drop table Address')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table Person (PersonId int, FirstName varchar(255), LastName varchar(255))",
                "Create table Address (AddressId int, PersonId int, City varchar(255), State varchar(255))",
                "Truncate table Person",
                "insert into Person (PersonId, LastName, FirstName) values ('1', 'Wang', 'Allen')",
                "Truncate table Address",
                "insert into Address (AddressId, PersonId, City, State) values ('1', '2', 'New York City', 'New York')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def combine(self):
        # left join 结构：
        # SELECT t1.name, t2.salary
        # FROM employee AS t1 INNER JOIN info AS t2 ON t1.name = t2.name;
        # https://dev.mysql.com/doc/refman/5.7/en/join.html

        try:
            sql1 = """
                select 
                    p.FirstName, p.LastName, a.City, a.State
                from 
                    Person as p left join Address as a 
                on 
                    p.PersonId = a.PersonId;
                """
            self.cs.execute(sql1)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.combine()
    print(ret)


if __name__ == '__main__':
    main()

