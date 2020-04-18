import pymysql


class Solution(object):
    """
有一个courses 表 ，有: student (学生) 和 class (课程)。
请列出所有超过或等于5名学生的课。例如,表:
+---------+------------+
| student | class      |
+---------+------------+
| A       | Math       |
| B       | English    |
| C       | Math       |
| D       | Biology    |
| E       | Math       |
| F       | Computer   |
| G       | Math       |
| H       | Math       |
| I       | Math       |
+---------+------------+
应该输出:
+---------+
| class   |
+---------+
| Math    |
+---------+
Note: 学生在每个课中不应被重复计算。
链接：https://leetcode-cn.com/problems/classes-more-than-5-students
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table courses')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists courses (student varchar(255), class varchar(255))",
                "Truncate table courses",
                "insert into courses (student, class) values ('A', 'Math')",
                "insert into courses (student, class) values ('B', 'English')",
                "insert into courses (student, class) values ('C', 'Math')",
                "insert into courses (student, class) values ('D', 'Biology')",
                "insert into courses (student, class) values ('E', 'Math')",
                "insert into courses (student, class) values ('F', 'Computer')",
                "insert into courses (student, class) values ('G', 'Math')",
                "insert into courses (student, class) values ('H', 'Math')",
                "insert into courses (student, class) values ('I', 'Math')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def classes(self):
        # 聚合函数，对一组值执行计算，并返回单个值，也被称为组函数
        # 常见聚合函数：max, min, sum, avg, count等
        # group by 结构
        # -----------------------------------
        # select column_name, aggregate_function(column_name)
        # from table_name
        # where column_name operator value
        # group by column_name;
        # -----------------------------------
        # 一般来说，group by 要结合聚合函数使用
        # 分组查询中，前面查询的字段除了用来分组的字段外，其余都必须用聚合函数
        # 如果前面是 select *，那么就必须给除了分组字段外其他所有字段加上聚合函数
        # 也就是要求 select * from courses group by xxx，* 其实就是唯一的字段且等于 xxx
        # 执行顺序：from -> where -> group by -> having -> select -> order by -> limit

        try:
            # sql = "select * from courses group by class"  # 错误！！why?? 假如同一个class对应了多个学生，那么该显示谁？
            sql1 = """
                select 
                    class 
                from 
                    (select 
                        class, count(class) as c 
                    from 
                        (select 
                            distinct student, class 
                        from 
                            courses) as table1 
                    group by 
                        class) as table2 
                where c >= 5;
                """  # 1、学生去重 2、学科分组 3、带条件查询   150 ms
            sql2 = """
                select 
                    class
                from
                    (select 
                        class, count(distinct student) as k
                    from 
                        courses
                    group by 
                        class) as table1
                where k >= 5;
                """  # 1、学科分组同时聚合不同学生 2、带条件查询  150 ms
            sql3 = """
                select 
                    class
                from 
                    courses
                group by 
                    class
                having 
                    count(distinct student) >= 5;
                """  # 240 ms
            self.cs.execute(sql3)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.classes()
    print(ret)


if __name__ == '__main__':
    main()
