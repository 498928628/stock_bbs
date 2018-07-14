import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
print('连接数据库成功', client)
# 设置要使用的数据库
mongodb_name = 'stock_list'
db = client[mongodb_name]
coll = db['top10_holders']

mongodb_name1 = 'xx'
db1 = client[mongodb_name1]
coll1 = db1['top10_holders']


coll1.insert(coll.find())