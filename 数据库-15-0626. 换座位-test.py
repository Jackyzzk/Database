import pymysql


class Solution(object):
    """
小美是一所中学的信息科技老师，她有一张 seat 座位表，
平时用来储存学生名字和与他们相对应的座位 id。
其中纵列的 id 是连续递增的，小美想改变相邻俩学生的座位。
你能不能帮她写一个 SQL query 来输出小美想要的结果呢？
+---------+---------+
|    id   | student |
+---------+---------+
|    1    | Abbot   |
|    2    | Doris   |
|    3    | Emerson |
|    4    | Green   |
|    5    | Jeames  |
+---------+---------+
假如数据输入的是上表，则输出结果如下：
+---------+---------+
|    id   | student |
+---------+---------+
|    1    | Doris   |
|    2    | Abbot   |
|    3    | Green   |
|    4    | Emerson |
|    5    | Jeames  |
+---------+---------+
如果学生人数是奇数，则不需要改变最后一个同学的座位。
链接：https://leetcode-cn.com/problems/exchange-seats
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table seat')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists seat(id int, student varchar(255))",
                "Truncate table seat",
                "insert into seat (id, student) values ('1', 'Abbot')",
                "insert into seat (id, student) values ('2', 'Doris')",
                "insert into seat (id, student) values ('3', 'Emerson')",
                "insert into seat (id, student) values ('4', 'Green')",
                "insert into seat (id, student) values ('5', 'Jeames')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def seats(self):
        try:
            sql1 = """
                select
                    cast(@seq := @seq + 1 as signed) as id, student
                from
                    (select
                        @k := id + if(id & 1, 1, -1) as id, student
                    from
                        seat
                    order by 
                        id) as t,
                    (select @seq := 0) as init
                """
            sql2 = """
                select
                    case when k & 1 and id = k
                    then id
                    when id & 1
                    then id + 1
                    else id - 1
                    end as id, 
                    student
                from
                    seat, (select max(id) as k from seat) as init
                order by 
                    id
                """
            sql3 = """
                select
                    if(k & 1 and id = k, k, cast((id + 1) ^ 1 - 1 as signed)) as id, 
                    student
                from
                    seat, (select max(id) as k from seat) as init
                order by 
                    id
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
    ret = test.seats()
    print(ret)


if __name__ == '__main__':
    main()

