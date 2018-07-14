from flask import (
    render_template,
    request,
    session,
    redirect,
    url_for,
    Blueprint,
)

from models.market_index import Market_index
from models.weight_action import Weight_action
from models.policy_action import Policy_action
from routes.index import login_client

main = Blueprint('topic', __name__)


# 获取最新指数价量异动
@main.route('/')
def index():
    # 获得最大id
    # query = {}
    # df = mongua.xx['Market_index'].find(query, {'id': 1, '_id': 0}).sort('id', -1).limit(1)
    # max_id = [x['id'] for x in df][0]
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = Market_index.find_all(user_id=uid)
    ss = Weight_action.find_all(user_id=uid)
    pp = Policy_action.find_all(user_id=uid)
    return render_template('topic/index.html', u=uu, s=ss, p=pp)


@main.route('/instruction1')
def instruction1():
    if login_client():
        return redirect(url_for('index.index'))
    return render_template('topic/instruction1.html')


@main.route('/instruction2')
def instruction2():
    if login_client():
        return redirect(url_for('index.index'))
    return render_template('topic/instruction2.html')


@main.route('/instruction3')
def instruction3():
    if login_client():
        return redirect(url_for('index.index'))
    return render_template('topic/instruction3.html')


@main.route('/instruction4')
def instruction4():
    if login_client():
        return redirect(url_for('index.index'))
    return render_template('topic/instruction4.html')

#指数价量异动页面显示
@main.route('/admin')
def admin():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = Market_index.find_all(user_id=uid)
    return render_template('topic/admin.html', u=uu)


@main.route('/weight')
def weight():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = Weight_action.find_all(user_id=uid)
    return render_template('topic/weight.html', u=uu)


@main.route('/policy')
def policy():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = Policy_action.find_all(user_id=uid)
    return render_template('topic/policy.html', u=uu)

#指数价量异动保存
@main.route('/market_index', methods=['POST'])
def market_index():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    uu = Market_index.index_register(form)
    return redirect(url_for('.admin'))


@main.route('/weight_index', methods=['POST'])
def weight_index():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    Weight_action.index_register(form)
    return redirect(url_for('.weight'))


@main.route('/policy_index', methods=['POST'])
def policy_index():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    Policy_action.index_register(form)
    return redirect(url_for('.policy'))


@main.route("/delete")
def delete():
    if login_client():
        return redirect(url_for('index.index'))
    id = int(request.args.get('id'))
    uid = session.get('user_id', -1)
    w = Weight_action.find_one(id=id, user_id=uid)
    Weight_action.delete(w)
    return redirect(url_for('.weight'))



@main.route("/delete1")
def delete1():
    if login_client():
        return redirect(url_for('index.index'))
    id = int(request.args.get('id'))
    uid = session.get('user_id', -1)
    w = Policy_action.find_one(id=id, user_id=uid)
    Policy_action.delete(w)
    return redirect(url_for('.policy'))



@main.route("/delete3")
def delete3():
    if login_client():
        return redirect(url_for('index.index'))
    id = int(request.args.get('id'))
    uid = session.get('user_id', -1)
    w = Market_index.find_one(id=id, user_id=uid)
    Market_index.delete(w)
    return redirect(url_for('.admin'))

