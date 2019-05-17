from drill.drill_utils import *

rs = drill_get("select * from mysql_250.main.sales t_0  inner join mysql_250.main.dates t_1 on t_0.date_id = t_1.id")

for i in rs:
    print(i)