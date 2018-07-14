from models.mongua import Mongua
from flask import session


class Policy_action1(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('section', str, ''),
        ('unusual_action', str, ''),
        ('link', str, ''),
        ('stock1', str, ''),
        ('stock2', str, ''),
        ('policy', str, ''),
    ]

    def __init__(self):
        pass

    @classmethod
    # 存入指数
    def index_register(cls, form):
        u = Policy_action1.new(form)
        u.id = session.get('user_id', -1)
        return u

