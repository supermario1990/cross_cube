# 从数据库中加载cube模型，并解析为对应sql


from pydrill.client import PyDrill
import json
from src.db.model_utils import *


# 获取表别名
def GetTbAlias(id):
    return 't' + str(id)


# 功能：对立方的关系进行分析
# 入参：事实表，关系
# 返回：join关系
# 说明：立方体一般来说有有两种关系，星型或者雪花模型。此函数将关系模型解析出来。
# 多张表通过关联，汇成一张平表
def AnalysisRelationship(fact_tb, relationship):
    tb_set = set()
    for i in json.loads(relationship)['joins']:
        tb_set.add(i['master'].split('.')[0])

    print(tb_set)
    master_id, full_master_tb = GetDbName(fact_tb)
    full_master_tb_alias = GetTbAlias(master_id)
    json_str = full_master_tb + ' ' + full_master_tb_alias

    def Analysis(fact_tb):
        tmp_str = ""
        master_tb = ""
        for i in json.loads(relationship)['joins']:
            master_tb = i['master'].split('.')[0]
            if master_tb == fact_tb:
                full_master_tb_field = i['master'].replace(master_tb, full_master_tb_alias)
                detail_tb = i['detail'].split('.')[0]
                datail_id, full_detail_tb = GetDbName(detail_tb)
                full_detail_tb_alias = GetTbAlias(datail_id)
                full_detail_tb_field = i['detail'].replace(detail_tb, full_detail_tb_alias)

                # 默认是inner join
                join_type = ' inner join '
                if i['join'] == 'left':
                    join_type = ' left join '
                elif i['join'] == 'right':
                    join_type = ' right join '

                tmp_str = tmp_str + join_type + full_detail_tb + ' ' + full_detail_tb_alias + ' on ' + \
                          full_master_tb_field + " = " + full_detail_tb_field
        return tmp_str

    json_str = json_str + Analysis(fact_tb)
    tb_set.remove(fact_tb)

    for n in tb_set:
        json_str = json_str + Analysis(n)

    return json_str


def cubeToSql(cube):
    # demo product, webshop, dates
    cube_rs = Select_Cubes_By_Name('dates')

    # 获取立方体维度和度量
    dims_json = cube_rs['cube_dims']
    measures_json = cube_rs['cube_measures']

    dims = json.loads(dims_json)
    measures = json.loads(measures_json)

    # 获取cube的数据模型信息
    data_model_id = cube_rs['data_model_id']

    datamodel_rs = Select_DataModel_By_ID(data_model_id)

    # 关联关系
    relationship = datamodel_rs['relationship']
    fact_tb = datamodel_rs['fact_tb']
    if relationship == None or relationship == "" or relationship == '{}':
        print("无关联关系，数据模型为单张逻辑表")
        _, source = GetDbName(fact_tb)
    elif relationship.find('joins') != -1:
        print('星型或者雪花模型')
        # 解析join关系
        master_tb = fact_tb
        master_id, full_master_tb = GetDbName(master_tb)
        full_master_tb_alias = GetTbAlias(master_id)
        json_str = full_master_tb + ' ' + full_master_tb_alias
        for i in json.loads(relationship)['joins']:
            full_master_tb_field = i['master'].replace(master_tb, full_master_tb_alias)
            detail_tb = i['detail'].split('.')[0]
            datail_id, full_detail_tb = GetDbName(detail_tb)
            full_detail_tb_alias = GetTbAlias(datail_id)
            full_detail_tb_field = i['detail'].replace(detail_tb, full_detail_tb_alias)
            if i['join'] == 'left':
                tmp_str = ' left join ' + full_detail_tb + ' ' + full_detail_tb_alias + ' on ' +  \
                           full_master_tb_field + " = " + full_detail_tb_field

        source = json_str + tmp_str

    print('source: ' + source)

    # 条件
    total_dims = json.loads(datamodel_rs['total_dims'])
    total_measures = json.loads(datamodel_rs['total_measures'])
    print(dims)
    print(measures)

    condition_dims_group_by = ",".join(dims['dimensions'])

    conditions = []

    for d in dims['dimensions']:
        for total_dim in total_dims['dimensions']:
            if d == total_dim['name'] and total_dim['label']:
                dim_str = d + " as " + total_dim['label']
                conditions.append(dim_str)

    for m in measures['measures']:
        for aggregate in total_measures['aggregates']:
            if m == aggregate['measure']:
                func = aggregate['function']
                tmp = '('+func + '('+aggregate['measure']+')'+')'
                for total_m in total_measures['measures']:
                    if total_m['name'] == m and total_m['label']:
                        tmp = tmp + ' as ' + total_m['label'] # measures 中的label作为别名

            conditions.append(tmp)

    print(conditions)

    condition_str = ",".join(conditions)

    sql = 'select ' + condition_str + " from " + source + " group by " + condition_dims_group_by
    print(sql)
    return sql


if __name__ == '__main__':
    # 从drill中查询数据
    drill = PyDrill(host='localhost', port=8047)

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    yelp_reviews = drill.query(cubeToSql('dates'))

    for result in yelp_reviews:
        print(result)