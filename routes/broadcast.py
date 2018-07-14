from models.mongua import mongua
from flask import session
import time

def last_upt():
    uid = session.get('user_id', -1)
    query = {
        'user_id': uid,
    }
    #调用时加一
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    doc = mongua.xx['upt']
    last_upt = doc.find_and_modify(**kwargs).get('upt', -1)
    print('last_upt', last_upt,type(last_upt),type(int(last_upt)))
    return last_upt

#复制管理员的内容,修改为当前user_id,并添加到当前库
def broadcast_cell(name, upt):
    #得到上一次更新的时间
    #对非管理员,更新时间大于upt的数据
    print('uouououououo',upt,type(upt))
    uid = session.get('user_id', -1)
    query = {
        'user_id':-10086,
        'deleted':False,
        'updated_time':{
            '$gt': upt
        },
    }
    field = {
        '_id': 0,
        'user_id':0,
    }
    print('1528592612', type(1528592612), type(upt),upt)
    copy1 = mongua.xx[name].find(query, field)
    copy1_list = list(copy1)
    print('copy1', copy1_list,type(copy1), len(copy1_list))
    #注意是0不是1,改了很久bug
    if len(copy1_list) > 0:
        mongua.xx[str(uid)].insert(mongua.xx[name].find(query, field))
        query = {
        }
        values = {
            '$set': {'user_id': uid}
        }
        mongua.xx[str(uid)].update_many(query, values,True)
        mongua.xx[name].insert(mongua.xx[str(uid)].find())
        mongua.xx[str(uid)].drop()


def broadcast_all():
    update_list = ["Height", 'Latent_calendar',
                   'Market_index', 'Market_index1',
                   'Policy_action', 'Policy_action1',
                   'Supervision', 'Weight_action', ]
    uid = session.get('user_id', -1)
    if uid == -10086:
        pass
    else:
        # 取得上一次时间
        upt = last_upt()
        for list in update_list:
            print('list', list)
            broadcast_cell(list, upt)

        # 更新时间到现在
        upt2 = int(time.time())
        print('******upt2', upt2)
        query = {
            'user_id': uid,
        }
        values = {
            '$set': {'upt': upt2}
        }
        mongua.xx['upt'].update_one(query, values, True)
        print('更新完所有表单')

