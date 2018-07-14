import time
from pymongo import MongoClient
from flask import session
mongua = MongoClient()

def validate_user():
    pass


def timestamp():
    return int(time.time())

def next_id(name):
    query = {
        'name': name,
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
    # 库.collections()
    doc = mongua.xx['data_id']
    # find_and_modify 是一个原子操作函数
    new_id = doc.find_and_modify(**kwargs).get('seq')
    print('new_id', new_id)
    return new_id





class Mongua(object):
    __fields__ = [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
        ('user_id', int, -1)
    ]

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    #mongo数据查询,得到所有类的列表
    def _find(cls, **kwargs):
        # 过滤掉被删除的元素,添加值False
        kwargs['deleted'] = False
        name = cls.__name__
        # flag_sort = '__sort'
        # sort = kwargs.pop(flag_sort, None)
        ds = mongua.xx[name].find(kwargs)
        # if sort is not None:
        #     ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    #生成model
    def _new_with_bson(cls, bson):
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def new(cls, form=None, **kwargs):
         name =  cls.__name__
         m = cls()
         fields = cls.__fields__.copy()
         fields.remove('_id')
         if form is None:
             form = {}
         for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
             #设为默认值
            else:
                setattr(m, k, v)
         #处理额外参数kwargs
         for k, v in kwargs.items():
             if hasattr(m, k):
                 setattr(m, k, v)
             else:
                 raise KeyError
         #写入默认数据
         m.id = next_id(name)
         ts = int(time.time())
         m.created_time = ts
         m.updated_time = ts
         m.type = name.lower()
         m.user_id = session.get('user_id')
         m.save()
         return m

         #保存一个实例的属性到mongo
    def save(self):
         # www.runoob.com/mongodb/mongodb-update.html
         name = self.__class__.__name__
         # save()通过传入的文档来替换已有的文档
         mongua.xx[name].save(self.__dict__)
         print('self.__dict__', self.__dict__)

    def delete(self):
        name = self.__class__.__name__
        query = {
            'id': self.id,
            'user_id': self.user_id,
        }
        values = {
            '$set':{'deleted': True}
        }
        mongua.xx[name].update_one(query, values)















