from flask import (
    render_template,
    request,
    session,
    redirect,
    url_for,
    Blueprint,
)

from models.policy_action1 import Policy_action1
from models.market_index1 import Market_index1
from models.latent_calendar import Latent_calendar
from models.height import Height

import time
from routes.index import login_client

main = Blueprint('topic1', __name__)


# 换仓总结页面
@main.route('/')
def index1():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = Market_index1.find_all(user_id=uid)
    # 显示最近两个月潜伏日历
    month = int(time.strftime('%m', time.localtime(time.time())))
    now_year = int(time.strftime('%Y', time.localtime(time.time())))
    ss1 = Latent_calendar.find_all(month=month, year=now_year)
    ss2 = Latent_calendar.find_all(month=month + 1, year=now_year)
    ss = ss1 + ss2
    pp = Policy_action1.find_all(user_id=uid)
    gg = Height.find_all(user_id=uid)
    return render_template('topic1/index1.html', u=uu, s=ss, p=pp, g=gg)


# 显示异动复盘页面
@main.route('/admin1')
def admin1():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = Market_index1.find_all(user_id=uid)
    return render_template('topic1/admin1.html', u=uu)


# 潜伏日历显示当前月份
@main.route('/weight1')
def weight1():
    if login_client():
        return redirect(url_for('index.index'))
    month = int(time.strftime('%m', time.localtime(time.time())))
    return redirect(url_for('.detail', id=month))


# 潜伏日历月份选择
@main.route('/weight1/<int:id>')
def detail(id):
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    now_year = int(time.strftime('%Y', time.localtime(time.time())))
    uu = Latent_calendar.find_all(month=id, year=now_year, user_id = uid)
    return render_template('topic1/weight1.html', u=uu)


@main.route('/policy1')
def policy1():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = Policy_action1.find_all(user_id=uid)
    return render_template('topic1/policy1.html', u=uu)


# 显示市场监管页面
@main.route('/height')
def height():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = Height.find_all(user_id=uid)
    return render_template('topic1/height.html', u=uu)


@main.route('/market_index1', methods=['POST'])
def market_index1():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    Market_index1.index_register(form)
    return redirect(url_for('.admin1'))


@main.route('/latent_calendar', methods=['POST'])
def latent_calendar():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    Latent_calendar.index_register(form)
    return redirect(url_for('.weight1'))


@main.route('/policy_index1', methods=['POST'])
def policy_index1():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    Policy_action1.index_register(form)
    return redirect(url_for('.policy1'))


@main.route('/height', methods=['POST'])
def height_index():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    Height.index_register(form)
    return redirect(url_for('.height'))


@main.route("/delete")
def delete():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    id = int(request.args.get('id'))
    w = Latent_calendar.find_one(id=id, user_id=uid)
    if True:
        Latent_calendar.delete(w)
        return redirect(url_for('.weight1'))
    else:
        return redirect(url_for('.weight1'))


@main.route("/delete1")
def delete1():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    id = int(request.args.get('id'))
    w = Policy_action1.find_one(id=id, user_id=uid)
    Policy_action1.delete(w)
    return redirect(url_for('.policy1'))


@main.route("/delete2")
def delete2():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    id = int(request.args.get('id'))
    w = Height.find_one(id=id, user_id=uid)
    Height.delete(w)
    return redirect(url_for('.height'))


@main.route("/delete3")
def delete3():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    id = int(request.args.get('id'))
    w = Market_index1.find_one(id=id, user_id=uid)
    Market_index1.delete(w)
    return redirect(url_for('.admin1'))
