from models.mongua import Mongua
from flask import session


class Market_index1(Mongua):
    __fields__ =__fields__ = Mongua.__fields__ + [
        ('result', str, ''),
        ('time', str, ''),
        ('way', str, ''),
        ('reason', str, ''),
    ]

    def __init__(self):
        pass

    @classmethod
    # 存入指数
    def index_register(cls, form):
        u = Market_index1.new(form)
        u.id = session.get('user_id', -1)
        return u




