import pymysql


class Solution(object):
    """
给定一个 salary 表，如下所示，有 m = 男性 和 f = 女性 的值。
交换所有的 f 和 m 值（例如，将所有 f 值更改为 m，反之亦然）。
要求只使用一个更新（Update）语句，并且没有中间的临时表。
注意，您必只能写一个 Update 语句，请不要编写任何 Select 语句。
| id | name | sex | salary |
|----|------|-----|--------|
| 1  | A    | m   | 2500   |
| 2  | B    | f   | 1500   |
| 3  | C    | m   | 5500   |
| 4  | D    | f   | 500    |
运行你所编写的更新语句之后，将会得到以下表:
| id | name | sex | salary |
|----|------|-----|--------|
| 1  | A    | f   | 2500   |
| 2  | B    | m   | 1500   |
| 3  | C    | f   | 5500   |
| 4  | D    | m   | 500    |
链接：https://leetcode-cn.com/problems/swap-salary
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table salary')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "create table if not exists salary (id int, name varchar(100), sex char(1), salary int)",
                "Truncate table salary",
                "insert into salary (id, name, sex, salary) values ('1', 'A', 'm', '2500')",
                "insert into salary (id, name, sex, salary) values ('2', 'B', 'f', '1500')",
                "insert into salary (id, name, sex, salary) values ('3', 'C', 'm', '5500')",
                "insert into salary (id, name, sex, salary) values ('4', 'D', 'f', '500')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def swap_salary(self):
        # update 表名称 set 列名称=新值 where 更新条件
        # -------------------------------
        # case when 的结构：
        # -------------------------------
        # case
        # when condition_1 then result_1
        # when condition_2 then result_2
        # ...
        # else result_n
        # end
        # 注意 result 只能是一个值而不能是语句

        try:
            sql1 = """
                update 
                    salary 
                set 
                    sex = 
                        case when sex = 'f' 
                        then 'm' 
                        else 'f' 
                        end;
                """
            sql2 = """
                update 
                    salary 
                set 
                    sex = 
                        case sex when 'f' 
                        then 'm' 
                        else 'f' 
                        end;
                """
            sql3 = """
                update 
                    salary 
                set 
                    sex = char(ascii('f') + ascii('m') - ascii(sex));
                """
            sql4 = """
                update 
                    salary 
                set 
                    sex = char(ascii('f') ^ ascii('m') ^ ascii(sex));
                """
            self.cs.execute(sql4)
            self.cs.execute("select * from salary")
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.swap_salary()
    print(ret)


if __name__ == '__main__':
    main()
