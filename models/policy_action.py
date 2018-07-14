from models.mongua import Mongua
from flask import session


class Policy_action(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('section', str, ''),
        ('weight_name', str, ''),
        ('hot_name', str, ''),
        ('position', str, ''),
        ('time', str, ''),
        ('policy', str, ''),
    ]

    def __init__(self):
        pass

    @classmethod
    # 存入指数
    def index_register(cls, form):
        u = Policy_action.new(form)
        u.id = session.get('user_id', -1)
        return u

