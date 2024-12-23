from easyrpa.script_exe.subprocess_python_script import subprocess_script_run
from transfer.flow_task_exe_res_dto_transfer import res_to_FlowTaskExeResDTO
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.enums.sys_log_type_enum import SysLogTypeEnum
from core import dispatch_task_core
import requests
from easyrpa.tools import request_tool,local_store_tools,logs_tool

class ScriptExeCore:
    def async_exe_script(self,flow_task:FlowTaskExeReqDTO,env_activate_command,python_interpreter,flow_exe_script,params,callback_url:str):
        try:
            # 执行脚本
            script_result = subprocess_script_run(env_activate_command=env_activate_command
                                                ,python_interpreter=python_interpreter
                                                ,script=flow_exe_script
                                                ,dict_args=params)

            # 构建回执对象
            result = res_to_FlowTaskExeResDTO(req=flow_task,res=script_result)

            # get current task id
            current_task_id = local_store_tools.get_data("task_id")

            # robot log report
            dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.INFO.value[1],message='robot exec ended,release task is ' + str(current_task_id),current_task_id=current_task_id)
            
            # remove task id
            local_store_tools.delete_data("task_id")

            # heartbeat inmediate
            dispatch_task_core.agent_heartbeat()

            # send result
            requests.post(callback_url, json=request_tool.request_base_model_json_builder(result))

        except Exception as e:
            # add log
            logs_tool.log_script_error(title="async_exe_script",message="async_exe_script run error",data=flow_task,exc_info=e)
            
            current_task_id = local_store_tools.get_data("task_id")

            # remove task id
            local_store_tools.delete_data("task_id")
            
            # heartbeat inmediate
            dispatch_task_core.agent_heartbeat()

            # robot log report
            dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.DEBUG.value[1],message='robot exec error , current task is ' + str(current_task_id) + '; message: ' + str(e),current_task_id=current_task_id)
            

        