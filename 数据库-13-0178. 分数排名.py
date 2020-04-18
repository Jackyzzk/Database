import pymysql


class Solution(object):
    """
编写一个 SQL 查询来实现分数排名。
如果两个分数相同，则两个分数排名（Rank）相同。请注意，
平分后的下一个名次应该是下一个连续的整数值。换句话说，名次之间不应该有“间隔”。
+----+-------+
| Id | Score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
| 6  | 3.65  |
+----+-------+
例如，根据上述给定的 Scores 表，你的查询应该返回（按分数从高到低排列）：
+-------+------+
| Score | Rank |
+-------+------+
| 4.00  | 1    |
| 4.00  | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.50  | 4    |
+-------+------+
链接：https://leetcode-cn.com/problems/rank-scores
    """
    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()

    def __del__(self):
        self.cs.execute('drop table Scores')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
                "Create table If Not Exists Scores (Id int, Score DECIMAL(3,2))",
                "Truncate table Scores",
                # "insert into Scores (Id, Score) values ('1', '0.0')"
                "insert into Scores (Id, Score) values ('1', '3.5')",
                "insert into Scores (Id, Score) values ('2', '3.65')",
                "insert into Scores (Id, Score) values ('4', '3.85')",
                "insert into Scores (Id, Score) values ('3', '4.0')",
                "insert into Scores (Id, Score) values ('5', '4.0')",
                "insert into Scores (Id, Score) values ('6', '3.65')"
            ]

        for sql in self.commands:
            self.cs.execute(sql)

    def rank(self):
        # Mysql 数据库中怎么设置变量
        # set @day = "2019-08-01";
        # set @day := "2019-08-01";
        # select @day := "2019-08-01";
        # 如果使用 select 关键词进行变量赋值时，不可以使用 = 号,因为会默认把它当作比较运算符，而不是赋值
        # -------------------------------------------
        # 语法：CAST (expression AS data_type)
        # 二进制，同带binary前缀的效果 : BINARY
        # 字符型，可带参数 : CHAR()
        # 日期 : DATE
        # 时间: TIME
        # 日期时间型 : DATETIME
        # 浮点数 : DECIMAL  注意这里不是 float
        # 整数 : SIGNED  注意这里不是 int， signed 表示有符号的 整型
        # 无符号整数 : UNSIGNED
        # --------------------------------------
        # 在MySQL中实现Rank高级并列排名函数
        # https://www.cnblogs.com/caicaizi/p/9803013.html

        try:
            sql1 = """
                select 
                    s1.Score, cast(s2.r as signed) as 'Rank'
                from
                    Scores as s1 
                    left join 
                        (select 
                            Score, @seq := @seq + 1 as r  # sequence 
                        from
                            (select distinct Score from Scores) as t1, 
                            (select  @seq := 0) as t2  # 去重并排列
                        order by 
                            Score DESC) as s2
                    on 
                        s1.Score = s2.Score
                order by 
                    s1.Score DESC 
                """
            sql2 = """
                select 
                    Score, cast(
                        case 
                        when @pre = Score
                        then @seq
                        when @pre := score  # 当score为0的时候，when @pre 判断为假，所以需要加一个else
                        then @seq := @seq + 1
                        else @seq := @seq + 1
                        end as signed) as 'Rank'
                from
                    Scores, (select @pre := NULL, @seq := 0) as init
                order by 
                    Score DESC 
                """
            # select 后出现的case when ，它不会在一步步执行中就把对应结果和 Score 组合起来
            # 而是保留 case when 结构，在最后排序完成后输出时，才把对应情况解析出来
            sql3 = """
                select
                    Score, 
                    cast(
                        if(@pre = Score, @seq, 
                            if(@pre := Score, @seq := @seq + 1, @seq := @seq + 1)) 
                        as signed) as 'Rank'
                from
                    Scores, (select @pre := NULL, @seq := 0) as init
                order by 
                    Score DESC
                """
            sql4 = """
                select
                    Score, 
                    cast(@seq := 
                        if(@pre = Score, @seq, 
                            if(@pre := Score, @seq + 1, @seq + 1)) 
                        as signed) as 'Rank'
                from
                    Scores, (select @pre := NULL, @seq := 0) as init
                order by 
                    Score DESC
                """
            sql5 = """
                select 
                    Score, 
                    cast(@seq := 
                        @seq + (@pre != (@pre := Score))  # 从左往右依次取到 @pre 的值放在表达式中，而不是地址的引用，顺序很关键
                        as signed) as 'Rank'
                from
                    Scores, (select @pre := -1, @seq := 0) as init
                order by 
                    Score DESC
                """
            sql5_test = """
                select 
                    if(0 = NULL, 1, NULL + 2), NULL = NULL
                """  # 输出(None, None)
            # NULL + 2 还是等于 NULL，判断里有 NULL 结果就是 NULL 无法判断，
            # 没有值你说我等于还是不等于？？所以 @pre 不能用 NULL 代替，只能用负数，-1就行
            self.cs.execute(sql5)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            self.__del__()
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.rank()
    print(ret)


if __name__ == '__main__':
    main()

