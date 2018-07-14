from models.mongua import Mongua
from flask import session


class Weight_action(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('section', str, ''),
        ('quantity', str, ''),
        ('central', str, ''),
        ('position', str, ''),
        ('line', str, ''),
        ('name', str, ''),
    ]

    def __init__(self):
        pass

    @classmethod
    # 存入指数
    def index_register(cls, form):
        u = Weight_action.new(form)
        u.id = session.get('user_id', -1)
        return u

