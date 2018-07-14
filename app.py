from flask import Flask
import config

app = Flask(__name__)
app.secret_key = config.secret_key

# 注册蓝图
# 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.topic1 import main as topic1_routes
from routes.topic2 import main as topic2_routes

app.register_blueprint(index_routes)
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(topic1_routes, url_prefix='/topic1')
app.register_blueprint(topic2_routes, url_prefix='/topic2')



# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载代码变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2001,
        threaded=True,
    )
    app.run(**config)
