import pymysql


class Solution(object):
    """
+-----------------+------------+------------+--------------+---------------+
| name            | continent  | area       | population   | gdp           |
+-----------------+------------+------------+--------------+---------------+
| Afghanistan     | Asia       | 652230     | 25500100     | 20343000      |
| Albania         | Europe     | 28748      | 2831741      | 12960000      |
| Algeria         | Africa     | 2381741    | 37100000     | 188681000     |
| Andorra         | Europe     | 468        | 78115        | 3712000       |
| Angola          | Africa     | 1246700    | 20609294     | 100990000     |
+-----------------+------------+------------+--------------+---------------+
如果一个国家的面积超过300万平方公里，或者人口超过2500万，那么这个国家就是大国家。
编写一个SQL查询，输出表中所有大国家的名称、人口和面积。
例如，根据上表，我们应该输出:
+--------------+-------------+--------------+
| name         | population  | area         |
+--------------+-------------+--------------+
| Afghanistan  | 25500100    | 652230       |
| Algeria      | 37100000    | 2381741      |
+--------------+-------------+--------------+
链接：https://leetcode-cn.com/problems/big-countries
    """

    def __init__(self):
        self.link = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    db='pycharm', charset='utf8')
        self.cs = self.link.cursor()
        self.commands = ''

    def __del__(self):
        self.cs.execute('drop table world')
        self.cs.close()
        self.link.close()

    def prepare(self):
        self.commands = \
            [
            "Create table If Not Exists World (name varchar(255), continent varchar(255), area int, population int, gdp bigint)",
            "Truncate table World",
            "insert into World (name, continent, area, population, gdp) values ('Afghanistan', 'Asia', '652230', '25500100', '20343000000')",
            "insert into World (name, continent, area, population, gdp) values ('Albania', 'Europe', '28748', '2831741', '12960000000')",
            "insert into World (name, continent, area, population, gdp) values ('Algeria', 'Africa', '2381741', '37100000', '188681000000')",
            "insert into World (name, continent, area, population, gdp) values ('Andorra', 'Europe', '468', '78115', '3712000000')",
            "insert into World (name, continent, area, population, gdp) values ('Angola', 'Africa', '1246700', '20609294', '100990000000')"
            ]
        for sql in self.commands:
            self.cs.execute(sql)

    def big_countries(self):
        try:
            sql1 = """
                select 
                    name, population, area 
                from 
                    world 
                where 
                    population > 25000000 or area > 3000000;
                """
            sql2 = """
                select 
                    name, population, area 
                from 
                    world 
                where 
                    area > 3000000 
                union select 
                    name, population, area 
                from 
                    world 
                where 
                    population > 25000000;
                """
            self.cs.execute(sql2)
            res = self.cs.fetchall()
            for x in res:
                print(x)
        except Exception as e:
            return e


def main():
    test = Solution()
    test.prepare()
    ret = test.big_countries()
    print(ret)


if __name__ == '__main__':
    main()
