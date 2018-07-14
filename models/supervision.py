from models.mongua import Mongua



class Supervision(Mongua):
    __fields__ =__fields__ = Mongua.__fields__ + [
        ('group', str, ''),
        ('name', str, ''),
        ('rank', str, ''),
        ('stock', str, ''),
        ('period', str, ''),
        ('tips', str, ''),
    ]

    def __init__(self):
        pass

    @classmethod
    # 存入指数
    def supervision_register(cls, form):
        u = Supervision.new(form)
        return u

