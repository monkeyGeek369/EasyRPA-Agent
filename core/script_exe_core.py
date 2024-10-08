from easyrpa.script_exe.subprocess_python_script import subprocess_script_run
from transfer.flow_task_exe_res_dto_transfer import res_to_FlowTaskExeResDTO
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
import requests
from easyrpa.tools import request_tool

class ScriptExeCore:
    def async_exe_script(self,flow_task:FlowTaskExeReqDTO,env_activate_command,python_interpreter,flow_exe_script,params,callback_url:str):
        
        # 执行脚本
        script_result = subprocess_script_run(env_activate_command=env_activate_command
                                              ,python_interpreter=python_interpreter
                                              ,script=flow_exe_script
                                              ,dict_args=params)

        # 构建回执对象
        result = res_to_FlowTaskExeResDTO(req=flow_task,res=script_result)

        # 回执结果推送
        self.script_exe_result_push(result,url=callback_url)

    def script_exe_result_push(self,result:FlowTaskExeResDTO,url:str):
        # 发送请求
        requests.post(url, json=request_tool.request_base_model_json_builder(result))