from flask import jsonify,Blueprint,request
from transfer import flow_task_exe_req_dto_transfer
from check import flow_task_exe_req_dto_check 
from easyrpa.script_exe.subprocess_python_script import subprocess_script_run
import json
from transfer.flow_task_exe_res_dto_transfer import res_to_FlowTaskExeResDTO
from agent_models.res.flow_task_exe_res_dto import FlowTaskExeResDTO
import platform


flow_task_bp =  Blueprint('flow_task',__name__)

@flow_task_bp.route('/flow/task/sync/exe', methods=['POST'])
def flow_task_sync_exe() -> FlowTaskExeResDTO:
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
        env_activate_command = None
        if platform.system() == "Windows":
            env_activate_command = f'conda activate {flow_task.flow_exe_env}'
        elif platform.system() == "Darwin":
            env_activate_command = f'source activate {flow_task.flow_exe_env}'
        elif platform.system() == "Linux":
            env_activate_command = f'source activate {flow_task.flow_exe_env}'
        else:
            return jsonify(FlowTaskExeResDTO(status=False,error_msg="operation sysytem is not support")),500
        python_interpreter = 'python'
        params = json.loads(flow_task.flow_standard_message)

        script_result = subprocess_script_run(env_activate_command,python_interpreter,flow_task.flow_exe_script,params)

        # 构建回执对象
        result = res_to_FlowTaskExeResDTO(flow_task,script_result)

        return jsonify(result.to_dict()), 200

    except (ValueError, json.JSONDecodeError) as e:
        return jsonify(FlowTaskExeResDTO(status=False,error_msg=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(FlowTaskExeResDTO(status=False,error_msg=str(e)).to_dict()), 500 
