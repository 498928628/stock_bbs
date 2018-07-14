from flask import (
    render_template,
    request,
    session,
    redirect,
    url_for,
    Blueprint,
)

from routes.broadcast import broadcast_all
from models.supervision import Supervision
from models.user import User
from routes.rat import name_find
from routes.rat import second_analyze


from models.mongua import mongua
from routes.index import current_user,login_client



main = Blueprint('topic2', __name__)


#统计组的类型
def group_cell():
    uid = session.get('user_id', -1)
    group_mongo = mongua.xx['Supervision'].aggregate([
        { '$match': {'deleted': False}},
        {'$match': {'user_id': uid}},
        {'$group': {
            '_id': {
                'group': '$group',
            },
        }},
    ])
    group_list = list(g['_id'].get('group') for g in group_mongo)
    print('group_list', group_list)
    return group_list

#获取最新指数价量异动
@main.route('/')
def index2():
    if login_client():
        return redirect(url_for('index.index'))
    return render_template('topic2/index2.html')

@main.route('/user')
def user():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    uu = User.find_by(id = uid)
    return render_template('topic2/user.html', u=uu)

@main.route('/ranklist')
def ranklist():
    if login_client():
        return redirect(url_for('index.index'))
    return render_template('topic2/ranklist.html')

@main.route('/update')
def update():
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    if uid == -10086:
        pass
    else:
        broadcast_all()
    return redirect(url_for('topic.index'))

@main.route('/analyze')
def analyze():
    if login_client():
        return redirect(url_for('index.index'))
    name_list = session.get('name_list','请先进行季报协同分析')
    return render_template('topic2/analyze.html',na = name_list)


@main.route('/front_running', methods = ['POST'])
def front_running():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    code=form['stock']
    qua = form['quarter']
    yea = int(form['year'])
    if qua == "{}.12.31-{}.03.31":
        quar = qua.format(int(yea-1), yea)
    else:
        quar = qua.format(yea, yea)
    coopers, name_set_list = name_find(code, quar)
    name_set_list = ','.join(name_set_list)
    cooper_new = {}
    for k,v in coopers.items():
        v = ','.join(v)
        cooper_new[k] = v
    session['name_list'] = name_set_list
    return render_template('topic2/front_running.html', uu = cooper_new, ss = name_set_list)

@main.route('/front_running2', methods = ['POST'])
def front_running2():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    name_str=form['list']
    name_list = name_str.split(',')
    name_set_all,all_coper_dict = second_analyze(name_list)
    cooper_new = {}
    for k,v in all_coper_dict.items():
        v[1] = ','.join(v[1])
        cooper_new[k] = v
    print('个人协同分析', cooper_new)
    return render_template('topic2/front_running2.html',
                           uu = cooper_new,
                           ss = ','.join(name_list),
                           pp = ','.join(name_set_all),
                           )


@main.route('/supervision_register', methods = ['POST'])
def supervision_register():
    if login_client():
        return redirect(url_for('index.index'))
    form = request.form
    group = form['group']
    Supervision.supervision_register(form)
    return redirect(url_for('.superv',groups = group))

@main.route('/supervision')
def supervision():
    if login_client():
        return redirect(url_for('index.index'))
    return redirect(url_for('topic2.superv', groups = 'groups'))

@main.route('/supervision/<groups>')
def superv(groups):
    if login_client():
        return redirect(url_for('index.index'))
    uid = session.get('user_id', -1)
    group_list = group_cell()
    uu = Supervision.find_all(user_id=uid, group=groups)
    return render_template('topic2/supervision.html', u =uu, s = group_list )


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    uid = session.get('user_id', -1)
    w = Supervision.find_one(id = id, user_id = uid)
    Supervision.delete(w)
    return redirect(url_for('.supervision'))

