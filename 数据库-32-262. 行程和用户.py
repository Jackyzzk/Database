import pymysql


class Solution(object):
    """
Trips 表中存所有出租车的行程信息。每段行程有唯一键 Id，Client_Id 和 Driver_Id 是 Users 表中 Users_Id 的外键。
Status 是枚举类型，枚举成员为 (‘completed’, ‘cancelled_by_driver’, ‘cancelled_by_client’)。
+----+-----------+-----------+---------+--------------------+----------+
| Id | Client_Id | Driver_Id | City_Id |        Status      |Request_at|
+----+-----------+-----------+---------+--------------------+----------+
| 1  |     1     |    10     |    1    |     completed      |2013-10-01|
| 2  |     2     |    11     |    1    | cancelled_by_driver|2013-10-01|
| 3  |     3     |    12     |    6    |     completed      |2013-10-01|
| 4  |     4     |    13     |    6    | cancelled_by_client|2013-10-01|
| 5  |     1     |    10     |    1    |     completed      |2013-10-02|
| 6  |     2     |    11     |    6    |     completed      |2013-10-02|
| 7  |     3     |    12     |    6    |     completed      |2013-10-02|
| 8  |     2     |    12     |    12   |     completed      |2013-10-03|
| 9  |     3     |    10     |    12   |     completed      |2013-10-03|
| 10 |     4     |    13     |    12   | cancelled_by_driver|2013-10-03|
+----+-----------+-----------+---------+--------------------+----------+
Users 表存所有用户。每个用户有唯一键 Users_Id。
Banned 表示这个用户是否被禁止，Role 则是一个表示（‘client’, ‘driver’, ‘partner’）的枚举类型。
+----------+--------+--------+
| Users_Id | Banned |  Role  |
+----------+--------+--------+
|    1     |   No   | client |
|    2     |   Yes  | client |
|    3     |   No   | client |
|    4     |   No   | client |
|    10    |   No   | driver |
|    11    |   No   | driver |
|    12    |   No   | driver |
|    13    |   No   | driver |
+----------+--------+--------+
写一段 SQL 语句查出 2013年10月1日 至 2013年10月3日 期间非禁止用户的取消率。
基于上表，你的 SQL 语句应返回如下结果，取消率（Cancellation Rate）保留两位小数。
取消率的计算方式如下：(被司机或乘客取消的非禁止用户生成的订单数量) / (非禁止用户生成的订单总数)
+------------+-------------------+
|     Day    | Cancellation Rate |
+------------+-------------------+
| 2013-10-01 |       0.33        |
| 2013-10-02 |       0.00        |
| 2013-10-03 |       0.50        |
+------------+-------------------+
链接：https://leetcode-cn.com/problems/trips-and-users
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Trips')
        self.cs.execute('drop table Users')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                """Create table If Not Exists Trips 
                        (Id int, Client_Id int, Driver_Id int, City_Id int, 
                        Status ENUM('completed', 'cancelled_by_driver', 'cancelled_by_client'), 
                        Request_at varchar(50))""",
                """Create table If Not Exists Users 
                        (Users_Id int, Banned varchar(50), Role ENUM('client', 'driver', 'partner'))""",
                "Truncate table Trips",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('1', '1', '10', '1', 'completed', '2013-10-01')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('2', '2', '11', '1', 'cancelled_by_driver', '2013-10-01')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('3', '3', '12', '6', 'completed', '2013-10-01')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('4', '4', '13', '6', 'cancelled_by_client', '2013-10-01')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('5', '1', '10', '1', 'completed', '2013-10-02')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('6', '2', '11', '6', 'completed', '2013-10-02')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('7', '3', '12', '6', 'completed', '2013-10-02')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('8', '2', '12', '12', 'completed', '2013-10-03')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('9', '3', '10', '12', 'completed', '2013-10-03')""",
                """insert into Trips (Id, Client_Id, Driver_Id, City_Id, Status, Request_at) 
                        values ('10', '4', '13', '12', 'cancelled_by_driver', '2013-10-03')""",
                "Truncate table Users",
                "insert into Users (Users_Id, Banned, Role) values ('1', 'No', 'client')",
                "insert into Users (Users_Id, Banned, Role) values ('2', 'Yes', 'client')",
                "insert into Users (Users_Id, Banned, Role) values ('3', 'No', 'client')",
                "insert into Users (Users_Id, Banned, Role) values ('4', 'No', 'client')",
                "insert into Users (Users_Id, Banned, Role) values ('10', 'No', 'driver')",
                "insert into Users (Users_Id, Banned, Role) values ('11', 'No', 'driver')",
                "insert into Users (Users_Id, Banned, Role) values ('12', 'No', 'driver')",
                "insert into Users (Users_Id, Banned, Role) values ('13', 'No', 'driver')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def trips(self):
        # CAST()函数将这个值转换为decimal类型，需要首先定义decimal值的精度与小数位数。
        # 精度是总的数字位数，包括小数点左边和右边位数的总和。而小数位数是小数点右边的位数。
        # AVG 函数返回数值列的平均值。NULL 值不包括在计算中。它会自动计算总数
        try:
            sql1 = """
                select 
                    Request_at as Day, 
                    cast(
                        sum(if(Status != 'Completed', 1, 0)) / count(Id) 
                            as decimal(3, 2)) as 'Cancellation Rate'
                from
                    Trips 
                    inner join
                        (select
                            Users_Id
                        from
                            Users
                        where
                            Banned = 'No' and Role = 'client') as init
                    on
                        Client_Id = Users_Id
                where
                    abs(datediff(Request_at, '2013-10-02')) < 2
                group by 
                    Request_at
                """
            sql2 = """
                select
                    Users_Id
                from
                    Users
                where
                    Banned = 'No' and Role = 'client'
            """
            sql3 = """
                select 
                    Request_at as Day, 
                    cast(
                        avg(Status != 'Completed')
                            as decimal(3, 2)) as 'Cancellation Rate'
                from
                    Trips 
                    inner join
                        (select
                            Users_Id
                        from
                            Users
                        where
                            Banned = 'No' and Role = 'client') as init
                    on
                        Client_Id = Users_Id
                where
                    abs(datediff(Request_at, '2013-10-02')) < 2
                group by 
                    Request_at
                """
            self.cs.execute(sql3)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            self.__del__()
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.trips()
    print(ret)


if __name__ == '__main__':
    main()


