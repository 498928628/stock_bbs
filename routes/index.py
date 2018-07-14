from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
)
import json
import urllib.request as ur
from models.user import User
from routes.broadcast import broadcast_all


main = Blueprint('index', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u

def login_client():
    uid = session.get('user_id', -1)
    print('uid',uid)
    if uid == -1:
        return True
    else:
        return False

#获取bing的壁纸
def get_one_photo():
        url=r'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=3'
        headers={
            'User-Agent': 'Mozilla / 4.0(compatible;MSIE6.0;Windows NT 5.1)'
        }
        request=ur.Request(url,headers=headers)
        response=ur.urlopen(request)
        html_byte=response.read()
        html_string=html_byte.decode('utf-8')
        #解析成字典形式,图片保存在images的key中:
        dict_json=json.loads(html_string)
        #得到images的key所包含的图片信息:
        list_photo=dict_json['images']
#       得到list_photo中的第三张图片组成的字典
        dict_three=list_photo[2]
        #得到图片的残缺url
        url_photo=dict_three['url']
        #将图片的残缺url组合成一个完整的url
        url_photo=r'http://cn.bing.com'+url_photo
        return url_photo


@main.route("/")
def index():
    url_photo = get_one_photo()
    return render_template("index.html", photo = url_photo)


@main.route("/register")
def register():
    # 用类函数来判断
    # u = User.register(form)
    url_photo = get_one_photo()
    return render_template("register.html", photo = url_photo)


@main.route('/post_register',methods=['POST'])
def post_register():
    form = request.form
    print('form',form)
    u = User.register(form)
    if u is not None:
        return redirect(url_for('.index'))
    else:
        er = '用户名或密码有误'
        url_photo = get_one_photo()
        return render_template("register.html", photo=url_photo, error =er)


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    print('login_form', form)
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.register'))
    else:
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        print('*********', u.id)
        if u.id == -10086:
            pass
        else:
            broadcast_all()
        return redirect(url_for('topic.index'))

