from application import flask_app
from application import base_app
from application import started_runner_app
import atexit

# 初始化线程池
base_app.init_thread_pool()
# 注册线程池shutdown
atexit.register(base_app.shutdown_thread_pool)

# run on app started
started_runner_app.run_on_started()

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5006, debug=True,use_reloader=False)
