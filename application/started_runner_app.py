from easyrpa.tools.thread_pool_util import ThreadPoolUtil
from core import dispatch_task_core

def run_on_started():
    # heartbeat
    ThreadPoolUtil.submit_task("common",dispatch_task_core.heartbeat_check_handler,params=123)
