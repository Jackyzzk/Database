import pymysql


class Solution(object):
    """
X 市建了一个新的体育馆，每日人流量信息被记录在这三列信息中：
序号 (id)、日期 (visit_date)、 人流量 (people)。
请编写一个查询语句，找出人流量的高峰期。高峰期时，至少连续三行记录中的人流量不少于100。
例如，表 stadium：
+------+------------+-----------+
| id   | visit_date | people    |
+------+------------+-----------+
| 1    | 2017-01-01 | 10        |
| 2    | 2017-01-02 | 109       |
| 3    | 2017-01-03 | 150       |
| 4    | 2017-01-04 | 99        |
| 5    | 2017-01-05 | 145       |
| 6    | 2017-01-06 | 1455      |
| 7    | 2017-01-07 | 199       |
| 8    | 2017-01-08 | 188       |
+------+------------+-----------+
对于上面的示例数据，输出为：
+------+------------+-----------+
| id   | visit_date | people    |
+------+------------+-----------+
| 5    | 2017-01-05 | 145       |
| 6    | 2017-01-06 | 1455      |
| 7    | 2017-01-07 | 199       |
| 8    | 2017-01-08 | 188       |
+------+------------+-----------+
每天只有一行记录，日期随着 id 的增加而增加。
链接：https://leetcode-cn.com/problems/human-traffic-of-stadium
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table stadium')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists stadium (id int, visit_date DATE NULL, people int)",
                "Truncate table stadium",
                "insert into stadium (id, visit_date, people) values ('1', '2017-01-01', '10')",
                "insert into stadium (id, visit_date, people) values ('2', '2017-01-02', '109')",
                "insert into stadium (id, visit_date, people) values ('3', '2017-01-03', '150')",
                "insert into stadium (id, visit_date, people) values ('4', '2017-01-04', '99')",
                "insert into stadium (id, visit_date, people) values ('5', '2017-01-05', '145')",
                "insert into stadium (id, visit_date, people) values ('6', '2017-01-06', '1455')",
                "insert into stadium (id, visit_date, people) values ('7', '2017-01-07', '199')",
                "insert into stadium (id, visit_date, people) values ('8', '2017-01-08', '188')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def stadium(self):
        # CAST()函数将这个值转换为decimal类型，需要首先定义decimal值的精度与小数位数。
        # 精度是总的数字位数，包括小数点左边和右边位数的总和。而小数位数是小数点右边的位数。
        # AVG 函数返回数值列的平均值。NULL 值不包括在计算中。它会自动计算总数
        # sql 语句中不能使用连续等于的判断：
        # 系统会先第一个等号语句，（其实是个布尔表达式）得到的结果是1或者0，然后再用0或者1去跟第二个对比得到最终的结果
        try:
            sql1 = """
                select
                    distinct s1.*
                from
                    stadium as s1, stadium as s2, stadium as s3
                where 
                    s1.people > 99 and s2.people > 99 and s3.people > 99
                    and 
                        (s1.id = s2.id - 1 and s1.id = s3.id - 2
                        or 
                        s1.id = s2.id + 1 and s1.id = s3.id - 1
                        or 
                        s1.id = s2.id + 1 and s1.id = s3.id + 2)
                order by 
                    s1.id
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
    ret = test.stadium()
    print(ret)


if __name__ == '__main__':
    main()


