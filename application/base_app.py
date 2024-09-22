from easyrpa.tools.thread_pool_util import ThreadPoolUtil


def init_thread_pool():
    ThreadPoolUtil.init_global_thread_pool("common", max_workers=5, thread_name_prefix='common')

def shutdown_thread_pool():
    ThreadPoolUtil.shutdown_global_thread_pool("common")