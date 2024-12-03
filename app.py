from application import flask_app
from application import base_app
import atexit
from core.dispatch_task_core import init_heartbaet_check

# 初始化定时任务
scheduler_tool = init_heartbaet_check()

# 注册job调度shutdown
atexit.register(scheduler_tool.shutdown)

# 初始化线程池
base_app.init_thread_pool()
# 注册线程池shutdown
atexit.register(base_app.shutdown_thread_pool)

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5006, debug=True,use_reloader=False)
