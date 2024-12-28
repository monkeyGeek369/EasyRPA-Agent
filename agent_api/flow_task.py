from flask import Blueprint
from check import flow_task_exe_req_dto_check 
from easyrpa.script_exe.subprocess_python_script import env_activate_command_builder
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.tools.request_tool import get_current_header
from core.script_exe_core import ScriptExeCore
from core import dispatch_task_core
from easyrpa.tools.request_tool import easyrpa_request_wrapper
import easyrpa.tools.debug_tools as my_debug
from easyrpa.tools.thread_pool_util import ThreadPoolUtil
from easyrpa.tools import logs_tool
from easyrpa.enums.sys_log_type_enum import SysLogTypeEnum
from configuration import app_config


flow_task_bp =  Blueprint('flow_task',__name__)

@flow_task_bp.route('/flow/task/async/exe', methods=['POST'])
@easyrpa_request_wrapper
def flow_task_async_exe(req:FlowTaskExeReqDTO):
    """flow task sync exe
    Args:
        FlowTaskExeReqDTO: req json data

    Returns:
        FlowTaskExeResDTO: exe result
    """
    # check task
    if dispatch_task_core.get_current_task_id() is not None:
        current_task_id = dispatch_task_core.get_current_task_id()
        dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.WARN.value[1],message='robot is running,current task is ' + str(current_task_id),current_task_id=current_task_id)
        return False

    try:
        task_id = req.get("task_id")

        # 构建请求对象
        flow_task = FlowTaskExeReqDTO(
            task_id=task_id,
            site_id=req.get("site_id"),
            flow_id=req.get("flow_id"),
            flow_code=req.get("flow_code"),
            flow_name=req.get("flow_name"),
            flow_rpa_type=req.get("flow_rpa_type"),
            flow_exe_env=req.get("flow_exe_env"),
            flow_standard_message=req.get("flow_standard_message"),
            flow_exe_script=req.get("flow_exe_script"),
            sub_source=req.get("sub_source"),
            max_exe_time=req.get("max_exe_time") if req.get("max_exe_time") is not None else 3600
        )

        # cache task id
        dispatch_task_core.set_current_task(req=flow_task)
        dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.INFO.value[1],message='robot get new task ' + str(task_id),current_task_id=task_id)

        # 校验请求对象
        flow_task_exe_req_dto_check.base_check(flow_task)

        # 执行脚本
        env_activate_command = env_activate_command_builder(flow_task.flow_exe_env)

        python_interpreter = 'python'
        
        # 构建执行参数
        params = my_debug.env_params_build(header=get_current_header()
                                            ,sub_source=flow_task.sub_source
                                            ,flow_standard_message=flow_task.flow_standard_message
                                            ,flow_config=None)
        # 获取控制台url
        control_url = app_config.EASYRPA_URL
        api_pash = app_config.TASK_RESULT_PUSH_API
        url = control_url + api_pash

        # 异步执行脚本
        script_exe = ScriptExeCore()
        ThreadPoolUtil.submit_task("common",script_exe.async_exe_script
                                ,flow_task=flow_task
                                ,env_activate_command=env_activate_command
                                ,python_interpreter=python_interpreter
                                ,flow_exe_script=flow_task.flow_exe_script
                                ,params=params
                                ,callback_url=url)
    except Exception as e:
        # add log
        logs_tool.log_script_error(title="flow_task_async_exe",message="task run error",data=None,exc_info=e)

        # report log
        current_task_id = dispatch_task_core.get_current_task_id()
        dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.DEBUG.value[1],message='robot exec error: task id is ' + str(current_task_id) + '; message: ' + str(e),current_task_id=current_task_id)

        # remove task id
        dispatch_task_core.release_current_task()

        # return
        return False
        

    # 构建回执对象
    return True
