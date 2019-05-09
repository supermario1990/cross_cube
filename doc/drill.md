# drill

## drill使用指南

## drill问题

1. 有的指令执行非常慢

   

```text
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.`TABLES`
ORDER BY TABLE_NAME DESC;
```

1,181 rows selected (977.421 seconds)

查了1181条数据，用时997秒

## pydrill

1. pydrill 使用 drill.query 时，sql最后不能带分号，否者报错
2. 