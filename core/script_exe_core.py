from easyrpa.script_exe.subprocess_python_script import subprocess_script_run
from transfer.flow_task_exe_res_dto_transfer import res_to_FlowTaskExeResDTO
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from application import flask_app
import requests

class ScriptExeCore:
    async def async_exe_script(self,flow_task:FlowTaskExeReqDTO,env_activate_command,python_interpreter,flow_exe_script,params):
        
        # 执行脚本
        script_result = subprocess_script_run(env_activate_command,python_interpreter,flow_exe_script,params)

        # 构建回执对象
        result = res_to_FlowTaskExeResDTO(flow_task,script_result)

        # 回执结果推送
        self.script_exe_result_push(result)

    def script_exe_result_push(self,result:FlowTaskExeResDTO):
        # 获取控制台url
        control_url = flask_app.config['EASYRPA_URL']

        # 发送请求
        api_pash = flask_app.config['TASK_RESULT_PUSH_API']
        requests.post(control_url + api_pash, json=result.to_dict())