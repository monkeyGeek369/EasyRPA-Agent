from flask import jsonify,Blueprint
from check import flow_task_exe_req_dto_check 
from easyrpa.script_exe.subprocess_python_script import env_activate_command_builder
from flask import current_app
from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.tools.request_tool import get_current_header
from core.script_exe_core import ScriptExeCore
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
import easyrpa.tools.debug_tools as my_debug
from easyrpa.tools.thread_pool_util import ThreadPoolUtil
from easyrpa.tools import local_store_tools


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
    # cache task id
    task_id = req.get("task_id")
    local_store_tools.add_data("task_id", task_id)

    try:
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
            sub_source=req.get("sub_source")
        )

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
        control_url = current_app.config['EASYRPA_URL']
        api_pash = current_app.config['TASK_RESULT_PUSH_API']
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
        # remove task id
        local_store_tools.delete_data("task_id")
        # raise exception
        raise e

    # 构建回执对象
    return True
