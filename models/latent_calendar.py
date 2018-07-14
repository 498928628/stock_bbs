from models.mongua import Mongua
from flask import session


class Latent_calendar(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('section', str, ''),
        ('link', str, ''),
        ('level', str, ''),
        ('start_time', str, ''),
        ('end_time', str, ''),
        ('stock', str, ''),
        ('month', int, ''),
        ('year', int, ''),
    ]

    def __init__(self):
        pass

    @classmethod
    # 存入指数
    def index_register(cls, form):
        u = Latent_calendar.new(form)
        u.id = session.get('user_id', -1)
        return u