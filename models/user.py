from models.mongua import Mongua
import hashlib



class User(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, ''),
    ]

    def __init__(self):
        pass

    #加密密码
    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    #返回摘要字符串
    def hashed_password(self, pwd):
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    @classmethod
    #用户名不能为重,密码大于6个字符
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if  30 > len(name) > 3 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    #密码验证
    def validate_login(cls, form):
        u = User()
        u.username = form.get('username', '')
        u.password =form.get('password', '')
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None