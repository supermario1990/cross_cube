import json

def GetDbName(fact_tb):
    return 1, fact_tb

def GetTbAlias(id):
    return 't1'

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
                if i['join'] == 'left':
                    tmp_str = tmp_str + ' left join ' + full_detail_tb + ' ' + full_detail_tb_alias + ' on ' + \
                              full_master_tb_field + " = " + full_detail_tb_field
        return tmp_str

    json_str = json_str + Analysis(fact_tb)
    tb_set.remove(fact_tb)

    for n in tb_set:
        json_str = json_str + Analysis(n)

    return json_str

rs = r'{"joins": [{"master": "sales.date_id","detail": "dates.id","join": "left"},{"master": "sales.ss_id","detail": "consumer.id","join": "left"}]}'

result = AnalysisRelationship('sales', rs)
print(result)
rs = r'{"joins": [{"master": "sales.date_id","detail": "dates.id","join": "left"},{"master": "dates.ss_id","detail": "consumer.id","join": "left"}]}'

result = AnalysisRelationship('sales', rs)
print(result)

