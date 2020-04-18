import pymysql


class Solution(object):
    """
编写一个 SQL 查询，查找 Person 表中所有重复的电子邮箱。
+----+---------+
| Id | Email   |
+----+---------+
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |
+----+---------+
根据以上输入，你的查询应返回以下结果：
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
说明：所有电子邮箱都是小写字母。
链接：https://leetcode-cn.com/problems/duplicate-emails
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Person')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists Person (Id int, Email varchar(255))",
                "Truncate table Person",
                "insert into Person (Id, Email) values ('1', 'a@b.com')",
                "insert into Person (Id, Email) values ('2', 'c@d.com')",
                "insert into Person (Id, Email) values ('3', 'a@b.com')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def emails(self):
        # 执行顺序：from -> where -> group by -> having -> select -> order by -> limit
        # having 子句的作用是筛选满足条件的组，即在分组之后过滤数据
        # 条件中经常包含聚组函数，使用having 条件显示特定的组，也可以使用多个分组标准进行分组
        # where字句无法与聚合函数一起使用，因为where子句的运行顺序排在第二，运行到where时，表还没有被分组。
        # 所以不能 where count(xx) ... ;
        # 聚合函数和临时表一样，后面都需要接一个 as 重新定义以便下次引用

        try:
            sql1 = """
                select 
                    Email 
                from 
                    (select 
                        Email, count(Id) as k
                    from 
                        Person 
                    group by 
                        Email) as table1
                where k > 1;
                """  # 150 ms
            sql2 = """
                select 
                    Email 
                from 
                    Person
                group by 
                    Email
                having 
                    count(id) > 1;
                """  # 150 ms
            self.cs.execute(sql1)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.emails()
    print(ret)


if __name__ == '__main__':
    main()

