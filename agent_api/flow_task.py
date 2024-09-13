from flask import jsonify,Blueprint,request
from transfer import flow_task_exe_req_dto_transfer
from check import flow_task_exe_req_dto_check 
from easyrpa.script_exe.subprocess_python_script import subprocess_script_run,env_activate_command_builder
import json
from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
import platform
from easyrpa.models.base.script_exe_param_model import ScriptExeParamModel
from easyrpa.tools.request_tool import get_current_header
from easyrpa.tools.transfer_tools import any_to_str_dict_first_level
from core.script_exe_core import ScriptExeCore


flow_task_bp =  Blueprint('flow_task',__name__)

@flow_task_bp.route('/flow/task/async/exe', methods=['POST'])
def flow_task_async_exe() -> FlowTaskExeResDTO:
    """flow task sync exe
    Args:
        FlowTaskExeReqDTO: req json data

    Returns:
        FlowTaskExeResDTO: exe result
    """
    try:
        # 获取请求对象
        req_json = request.get_json()
        flow_task = flow_task_exe_req_dto_transfer.req_to_FlowTaskExeReqDTO(req_json)

        # 校验请求对象
        flow_task_exe_req_dto_check.base_check(flow_task)

        # 执行脚本
        env_activate_command = env_activate_command_builder(flow_task.flow_exe_env)

        python_interpreter = 'python'

        # 构建脚本执行参数
        script_params = ScriptExeParamModel()
        script_params.header = get_current_header()
        script_params.source = flow_task.sub_source
        script_params.standard = json.loads(flow_task.flow_standard_message)
        params = any_to_str_dict_first_level(script_params)

        # 异步执行脚本
        ScriptExeCore.async_exe_script(flow_task,env_activate_command,python_interpreter,flow_task.flow_exe_script,params)

        # 构建回执对象
        return jsonify(FlowTaskExeResDTO(status=True,error_msg="调用agent成功").to_dict()), 200

    except (ValueError, json.JSONDecodeError) as e:
        return jsonify(FlowTaskExeResDTO(status=False,error_msg=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(FlowTaskExeResDTO(status=False,error_msg=str(e)).to_dict()), 500 
