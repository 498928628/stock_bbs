from models.mongua import Mongua
from flask import session


class Height(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('rose', str, ''),
        ('stock', str, ''),
        ('section', str, ''),
        ('status', str, ''),
        ('stock2', str, ''),
        ('policy', str, ''),
    ]

    def __init__(self):
        pass

    @classmethod
    # 存入指数
    def index_register(cls, form):
        u = Height.new(form)
        u.id = session.get('user_id', -1)
        return u
