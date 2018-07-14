from difflib import SequenceMatcher
import pymongo
import datetime
import random
from collections import defaultdict

# 连接mongo数据库,主机是本机,端口是默认的端口
client = pymongo.MongoClient("mongodb://localhost:27017")
print('连接数据库成功', client)

# 设置要使用的数据库
mongodb_name = 'xx'
db = client[mongodb_name]
coll = db['top10_holders']


#国家队
nation_cooperator = ['中央汇金投资有限责任公司',
                     "香港中央结算有限公司",
                     '中央汇金资产管理有限公司',
                     '中国证券金融股份有限公司',
                     '博时基金-农业银行-博时中证金融资产管理计划',
                     '工银瑞信基金-农业银行-工银瑞信中证金融资产管理计划',
                     '中欧基金-农业银行-中欧中证金融资产管理计划',
                     '嘉实基金-农业银行-嘉实中证金融资产管理计划',
                     '南方基金-农业银行-南方中证金融资产管理计划',
                     '华夏基金-农业银行-华夏中证金融资产管理计划',
                     '易方达基金-农业银行-易方达中证金融资产管理计划',
                     '广发基金-农业银行-广发中证金融资产管理计划',
                     '大成基金-农业银行-大成中证金融资产管理计划',
                     '银华基金-农业银行-银华中证金融资产管理计划',
                     '北京凤山投资有限责任公司',
                     '北京坤藤投资有限责任公司',
                     '梧桐树投资平台有限责任公司',
                     '中国银行股份有限公司-招商丰庆灵活配置混合型发起式证券投资基金',
                     '中国农业银行股份有限公司-易方达瑞惠灵活配置混合型发起式证券投资基金',
                     '中国工商银行股份有限公司-南方消费活力灵活配置混合型发起式证券投资基金',
                     '中国工商银行股份有限公司-嘉实新机遇灵活配置混合型发起式证券投资基金',
                     '中国银行股份有限公司-华夏新经济灵活配置混合型发起式证券投资基金',
                     '中央汇金资产管理有限责任公司',
                     '中国国际金融股份有限公司',
                     ]

# 更多的限制条件在实践中添加
other_fund = ['全国社保基金', '指数', '中国人寿', '新华人寿', '信用交易担保', '定增', '员工持股', '集团', 'LOF', '全国社会保障基金', '(LOF)', '中国平安人寿',
              '保险', '混合型证券投资基金', '型证券投资基金', '中央汇金','大盘','混合型',
              '约定购回', '股指', '企业年金', '新股申购', '国有资产', 'ETF', '中央结算', '证券股份有限公司']

# 得到季度code的不重名holders
def code_find1(code, period):
    name20 = []
    time1, time2 = period.split('-')
    time1 = datetime.datetime.strptime(time1, '%Y.%m.%d')
    time2 = datetime.datetime.strptime(time2, '%Y.%m.%d')
    query = {
        'code': code,
        '$or': [
            {
                'quarter': time1,
            },
            {
                'quarter': time2,
            }
        ]
    }
    field = {
        'code': code,
        'name': 1,
        '_id': 0,
    }
    df = list(coll.find(query, field))
    name_list = list(set([x['name'] for x in df]))
    name_dic = {}
    name_dic[code] = name_list
    name20.append(name_dic)
    print('连续两期股东', name20)
    return name20


# 找name所买过的code
def name_find(code, period):
    for i in code_find1(code, period):
        for k, v in i.items():
            code = k
            name_list = v
            rng = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3))
            col = db[code + rng]
            n = 0
            while len(name_list) > n:
                name = name_list[n]
                query = {
                    'name': name,
                    'sharetype': '流通A股',
                }
                field = {
                    'code': 1,
                    'name': 1,
                    'quarter': 1,
                    '_id': 0,
                }
                try:
                    if other_funds(name):
                        col.insert(db.top10_holders.find(query, field))
                except:
                    print('为非流通股股东')
                finally:
                    n += 1
            col.delete_many({'code': code})
            from_code = code
            return cooperator_first(reclean(col), from_code)
    print('全部完成协同分析')

#将20个holders操作过的个股,统计单个code出现过的人数
def reclean(col):
    namecode = col.aggregate([
        {'$group': {
            '_id': {
                'code': '$code', 'name': '$name'
            },
            # 'count': {
            #     '$sum': 1
            # }
        }},
        # {
        #     '$match': {'count': {'$gt': 0}}
        # }
    ])
    namecode_list = list(namecode)
    col.drop()
    print('个股出现人数', namecode_list)
    return namecode_list



# name_set_list ['张长虹', '李玉民', '王玫', '张婷', '张志宏', '易小强']
def cooperator_first(namecode_list, from_code):
    d = defaultdict(list)
    for i in namecode_list:
        namecode_dic = i['_id']
        code = namecode_dic['code']
        name = namecode_dic['name']
        if other_funds(name):
            d[code].append(name)
    name_list = []
    front_running = {}
    for i in d:
        if len(d.get(i)) > 1:
            name_list = name_list + d.get(i)
            print('协同股东', i, d.get(i))
            front_running[i] = d.get(i)
            # u = {
            #     'coper_code': i,
            #     'cooperator': d.get(i),
            #     'from_code': from_code,
            # }
            # db.cooperation.insert(u)
    name_set_list = list(set(name_list))
    print('当季协同股东', front_running)
    print('#######################协同姓名表', name_set_list)
    return front_running,name_set_list


# 去除大型金融机构
def other_funds(name):
    nn = 0
    for x in other_fund:
        if name.find(x) >= 0:
            nn = -1
    if nn == 0 and name not in nation_cooperator:
        return True
    else:
        return False

#添加国家队到MongoDB
# http://funds.hexun.com/2017-11-03/191491903.html
def add_topname(top_name, from_code):
    nation_cooperator = ['中央汇金投资有限责任公司',
                         "香港中央结算有限公司",
                         '中央汇金资产管理有限公司',
                         '中国证券金融股份有限公司',
                         '博时基金-农业银行-博时中证金融资产管理计划',
                         '工银瑞信基金-农业银行-工银瑞信中证金融资产管理计划',
                         '中欧基金-农业银行-中欧中证金融资产管理计划',
                         '嘉实基金-农业银行-嘉实中证金融资产管理计划',
                         '南方基金-农业银行-南方中证金融资产管理计划',
                         '华夏基金-农业银行-华夏中证金融资产管理计划',
                         '易方达基金-农业银行-易方达中证金融资产管理计划',
                         '广发基金-农业银行-广发中证金融资产管理计划',
                         '大成基金-农业银行-大成中证金融资产管理计划',
                         '银华基金-农业银行-银华中证金融资产管理计划',
                         '北京凤山投资有限责任公司',
                         '北京坤藤投资有限责任公司',
                         '梧桐树投资平台有限责任公司',
                         '中国银行股份有限公司-招商丰庆灵活配置混合型发起式证券投资基金',
                         '中国农业银行股份有限公司-易方达瑞惠灵活配置混合型发起式证券投资基金',
                         '中国工商银行股份有限公司-南方消费活力灵活配置混合型发起式证券投资基金',
                         '中国工商银行股份有限公司-嘉实新机遇灵活配置混合型发起式证券投资基金',
                         '中国银行股份有限公司-华夏新经济灵活配置混合型发起式证券投资基金', ]
    for name in nation_cooperator:
        query = {
            'top_name': top_name,
            'name': name,
            'from_code': from_code,
        }
        db.top_name.insert(query)
    print('完成list的top_name添加')


# 个人分析
def frequency(namecode_list, holder):
    d = defaultdict(list)
    nameca = []
    for i in namecode_list:
        namecode_dic = i['_id']
        name = namecode_dic['name']
        nameca.append(name)
    namecache = list(set(nameca))
    for i in namecode_list:
        namecode_dic = i['_id']
        code = namecode_dic['code']
        name = namecode_dic['name']
        # 处理信托,私募产品的关联
        ''''''''''''''''''
        index_list = []
        for x in namecache:
            if similarity(name, x) > 0.8:
                index_list.append(namecache.index(x))
                index_list.sort()
        name = '&'.join([namecache[x] for x in index_list])
        d[name].append(code)
    name_list = []
    all_dict = {}
    for i in d:
        if len(list(set(d.get(i)))) > 1:
            name_list.append(i)
            print('关联操作', holder,i, d.get(i))
            all_dict[i]=[holder, d.get(i)]
            # u = {
            #     'coper_code': d.get(i),
            #     'cooperator': i,
            # }
            # db.cooperation.insert(u)
    name_set = list(set(name_list))
    print('关联操作总表', all_dict)
    return name_set,all_dict


def similarity(strA, strB):
    similarity = SequenceMatcher(lambda x: x == " ", strA, strB).ratio()
    return similarity

#个人关联分析
def single_holder(holder):
    query = {
        'name': holder,
        'sharetype': '流通A股',
    }
    field = {
        'code': 1,
        # 'name': 1,
        'quarter': 1,
        '_id': 0,
        # '$not':{'name':name}
    }
    df = list(coll.find(query, field))
    rng = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3))
    name_coll = db[holder + rng]
    for i in df:
        query = i
        field = {
            'code': 1,
            'name': 1,
            '_id': 0,
        }
        try:
            name_coll.insert(coll.find(query, field))
        except:
            print('个人名字有误')
    name_coll.delete_many({'name': holder})
    for x in other_fund:
        name_coll.delete_many({"name": {'$regex': "{}".format(x)}})
        print('**********************************************************************')
    return frequency(reclean(name_coll), holder)


def second_analyze(name_list):
    name_set_cache =[]
    all_coper_dict = {}
    for name in name_list:
        print('name', name)
        name_set, all_dict = single_holder(name)
        print('name_set%%%%',name_set,all_dict)
        name_set_cache = name_set_cache + name_set
        all_coper_dict = dict(all_coper_dict,**all_dict)
    name_set_all = list(set(name_set_cache))
    return name_set_all,all_coper_dict





