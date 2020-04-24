import pymysql


class Solution(object):
    """
部门表 Department：
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| revenue       | int     |
| month         | varchar |
+---------------+---------+
(id, month) 是表的联合主键。
这个表格有关于每个部门每月收入的信息。
月份（month）可以取下列值 ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]。
编写一个 SQL 查询来重新格式化表，使得新的表中有一个部门 id 列和一些对应 每个月 的收入（revenue）列。
查询结果格式如下面的示例所示：
Department 表：
+------+---------+-------+
| id   | revenue | month |
+------+---------+-------+
| 1    | 8000    | Jan   |
| 2    | 9000    | Jan   |
| 3    | 10000   | Feb   |
| 1    | 7000    | Feb   |
| 1    | 6000    | Mar   |
+------+---------+-------+
查询得到的结果表：
+------+-------------+-------------+-------------+-----+-------------+
| id   | Jan_Revenue | Feb_Revenue | Mar_Revenue | ... | Dec_Revenue |
+------+-------------+-------------+-------------+-----+-------------+
| 1    | 8000        | 7000        | 6000        | ... | null        |
| 2    | 9000        | null        | null        | ... | null        |
| 3    | null        | 10000       | null        | ... | null        |
+------+-------------+-------------+-------------+-----+-------------+
注意，结果表有 13 列 (1个部门 id 列 + 12个月份的收入列)。
链接：https://leetcode-cn.com/problems/reformat-department-table
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Department')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists Department (id int, revenue int, month varchar(5))",
                "Truncate table Department",
                "insert into Department (id, revenue, month) values ('1', '8000', 'Jan')",
                "insert into Department (id, revenue, month) values ('2', '9000', 'Jan')",
                "insert into Department (id, revenue, month) values ('3', '10000', 'Feb')",
                "insert into Department (id, revenue, month) values ('1', '7000', 'Feb')",
                "insert into Department (id, revenue, month) values ('1', '6000', 'Mar')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def department(self):
        try:
            sql1 = """
                select
                    id,
                    max(if(month = 'Jan', revenue, null)) as Jan_Revenue,
                    max(if(month = 'Feb', revenue, null)) as Feb_Revenue,
                    max(if(month = 'Mar', revenue, null)) as Mar_Revenue,
                    max(if(month = 'Apr', revenue, null)) as Apr_Revenue,
                    max(if(month = 'May', revenue, null)) as May_Revenue,
                    max(if(month = 'Jun', revenue, null)) as Jun_Revenue,
                    max(if(month = 'Jul', revenue, null)) as Jul_Revenue,
                    max(if(month = 'Aug', revenue, null)) as Aug_Revenue,
                    max(if(month = 'Sep', revenue, null)) as Sep_Revenue,
                    max(if(month = 'Oct', revenue, null)) as Oct_Revenue,
                    max(if(month = 'Nov', revenue, null)) as Nov_Revenue,
                    max(if(month = 'Dec', revenue, null)) as Dec_Revenue
                from
                    Department
                group by 
                    id
                """  # 分组加聚合
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
    ret = test.department()
    print(ret)


if __name__ == '__main__':
    main()

