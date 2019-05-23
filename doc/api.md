# 接口文档

## cube模型

```json
{
  "uuid": "3ec0147d-47c9-5e5d-382e-bfb6ae1414a9",
  "last_modified": 1552969573435,
  "version": "2.6.1.0",
  "name": "sales_model",
  "description": "销售信息模型",
  "fact_table": "mysql_250.sales",
  "alias": "t_0",
  "lookups": [
    {
      "index": 1,
      "table": "mysql_250.dates",
      "kind": "LOOKUP",
      "alias": "t_1",
      "join": {
        "type": "inner",
        "primary_key": "t_1.id",
        "foreign_key": "t_0.date_id"
      }
    }
  ],
  "dimensions": [
    {
      "table": "t_0",
      "columns": [
        {"name":"id", "alias": "id"},
        {"name": "date_id", "alias": "date_id"},
        {"name": "customer_id", "alias": "customer_id"},
        {"name": "product_id", "alias": "product_id"},
        {"name": "country_id", "alias": "country_id"}
      ]
    },
    {
      "table": "t_1",
      "columns": [
        {"name": "id", "alias": "id"},
        {"name": "date_year", "alias": "year"},
        {"name": "date_quarter", "alias": "quarter"},
        {"name": "date_month", "alias": "month"},
        {"name": "date_day", "alias": "day"},
        {"name": "date_week", "alias": "week"}
      ]
    }
  ],
  "measuers": [
    {
      "table": "t_0",
      "columns": [
        {"name": "quantity", "alias": "quantity", "func": "sum"},
        {"name": "price_total", "alias": "price_total", "func": "sum"},
        {"name": "test", "alias": "test", "func": "sum"}
      ]
    }
  ]
}
```

上面的json文件描述了一个cube模型

| **字段**      | **说明**               | **附加说明**                                                 |
| ------------- | :--------------------- | ------------------------------------------------------------ |
| uuid          | cube的id               |                                                              |
| last_modified | 最后修改时间           |                                                              |
| version       | 版本                   |                                                              |
| name          | cube名字               |                                                              |
| description   | 描述                   |                                                              |
| fact_table    | 事实表，数据源+表      |                                                              |
| alias         | 别名，事实表固定为 t_0 |                                                              |
| lookups       | 关联关系               | index： 表索引<br />table：表名<br />kind：保留<br />alias：别名<br />join：连接关系 |
| dimensions    | 维度                   |                                                              |
| measuers      | 度量                   | columns：列<br />func：聚合函数                              |

## 接口

### 创建数据集

***URI：/olap/dataset/:name***

***POST***

| **入参**   | **说明**            | **举例**        |
| ---------- | ------------------- | --------------- |
| fact_table | 事实表              | mysql_250.sales |
| lookups    | 关联关系(可选)      | [见下方]([1])       |
| **出参**   | **说明**            |                 |
| data       | cube模型            |                 |
| msg        | 信息                |                 |
| success    | false失败，true成功 |                 |

> [1] lookups 入参举例
>
> ```json
> {
> 	"lookups": [
> 		{
> 			"index": 1,
> 			"table": "mysql_250.dates",
> 			"join": {
> 				"type": "inner",
> 				"primary_key": "t_1.id",
> 				"foreign_key": "t_0.date_id"
> 			}
> 		}
> 	]
> }
> ```
>
> 

### 修改数据集

***URI ：/olap/dataset/:name***

***PUT***

| **入参**   | **说明**            | **举例**        |
| ---------- | ------------------- | --------------- |
| fact_table | 事实表              | mysql_250.sales |
| lookups    | 关联关系（可选）    | 如上[1]         |
| rename     | 重命名（可选）      | name1           |
| dims       | 维度（可选）        | 见下[2]         |
| measures   | 度量（可选）        | 见下[3]         |
| **出参**   | **说明**            |                 |
| data       | cube模型            |                 |
| msg        | 信息                |                 |
| success    | false失败，true成功 |                 |

> [2] dims 入参举例
>
> ```
> {
> 	"dimensions": [
> 		{
> 			"columns": [
> 				{
> 					"alias": "",
> 					"name": "id"
> 				},
> 				{
> 					"alias": "",
> 					"name": "date_id"
> 				},
> 				{
> 					"alias": "",
> 					"name": "customer_id"
> 				},
> 				{
> 					"alias": "",
> 					"name": "product_id"
> 				},
> 				{
> 					"alias": "",
> 					"name": "country_id"
> 				}
> 			],
> 			"alias": "t_0",
> 			"table":"mysql_250.sales"
> 		},
> 		{
> 			"columns": [
> 				{
> 					"alias": "",
> 					"name": "id"
> 				},
> 				{
> 					"alias": "",
> 					"name": "date_year"
> 				}
> 			],
> 			"table": "t_1",
> 			"table":"mysql_250.dates"
> 		}
> 	]
> }
> ```
>
> [3] measures 入参举例
>
> ```json
> {
> 	"measures": [
> 		{
> 			"columns": [
> 				{
> 					"alias": "",
> 					"name": "quantity"
> 				},
> 				{
> 					"alias": "",
> 					"name": "price_total"
> 				},
> 				{
> 					"alias": "",
> 					"name": "test"
> 				}
> 			],
> 			"alias": "t_0",
> 			"table":"mysql_250.sales"
> 		},
> 		{
> 			"columns": [
> 				{
> 					"alias": "",
> 					"name": "date_quarter"
> 				},
> 				{
> 					"alias": "",
> 					"name": "date_month"
> 				},
> 				{
> 					"alias": "",
> 					"name": "date_day"
> 				},
> 				{
> 					"alias": "",
> 					"name": "date_week"
> 				}
> 			],
> 			"table": "t_1",
> 			"table":"mysql_250.dates"
> 		}
> 	]
> }
> ```

### 删除数据集

***URI ：/olap/dataset/:name***

***DELETE***

入参无，出参同上

### 查询数据集

***URI ：/olap/dataset/:name***

***GET***

入参无，出参同上

### 查询立方体

***URI ：/olap/cube/:name***

***POST***

| **入参** | **说明**                                                     | **举例** |
| -------- | ------------------------------------------------------------ | -------- |
| dim      | 维度（可选）                                                 | 见上[2]  |
| measures | 指标（可选）                                                 | 见上[3]  |
| filter   | 过滤条件（可选）                                             | 见下[4]  |
| **出参** | **说明**                                                     |          |
| data     | attemptedAutoLimit：限制条数<br />columns: 字段集合<br />metadata:字段类型<br />rows：数据集<br />sql：查询sql |          |
| msg      | 信息                                                         |          |
| success  | false失败,true成功                                           |          |

