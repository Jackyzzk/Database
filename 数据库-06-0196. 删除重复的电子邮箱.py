import pymysql


class Solution(object):
    """
编写一个 SQL 查询，来删除 Person 表中所有重复的电子邮箱，重复的邮箱里只保留 Id 最小 的那个。
+----+------------------+
| Id | Email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
Id 是这个表的主键。
例如，在运行你的查询语句之后，上面的 Person 表应返回以下几行:
+----+------------------+
| Id | Email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
执行 SQL 之后，输出是整个 Person 表。
使用 delete 语句。
链接：https://leetcode-cn.com/problems/delete-duplicate-emails
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
                "insert into Person (Id, Email) values ('1', 'john@example.com')",
                "insert into Person (Id, Email) values ('2', 'bob@example.com')",
                "insert into Person (Id, Email) values ('3', 'john@example.com')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def emails(self):
        # delete 结构：
        # delete from table_name
        # where conditions
        # If you declare an alias for a table, you must use the alias when referring to the table:
        # DELETE t1 FROM test AS t1, test2 WHERE ...

        try:
            sql1 = """
                delete 
                    p1 
                from 
                    Person as p1, Person as p2 
                where 
                    p1.Email = p2.Email and p1.Id > p2.Id;
                """  # 自连接  700 ms
            sql2 = """
                delete from
                    Person
                where 
                    Id not in 
                        (select 
                            Id 
                        from 
                            (select 
                                min(Id) as Id
                            from 
                                Person 
                            group by 
                                Email) as table1);
                """  # 两层子查询  500 ms
            self.cs.execute(sql2)
            self.cs.execute("select * from Person")
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

