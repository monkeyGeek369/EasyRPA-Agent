from easyrpa.script_exe.subprocess_python_script import subprocess_script_run
from transfer.flow_task_exe_res_dto_transfer import res_to_FlowTaskExeResDTO
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.enums.sys_log_type_enum import SysLogTypeEnum
from core import dispatch_task_core
import requests
from easyrpa.tools import request_tool,logs_tool

class ScriptExeCore:
    def async_exe_script(self,flow_task:FlowTaskExeReqDTO,env_activate_command,python_interpreter,flow_exe_script,params,callback_url:str):
        try:
            logs_tool.log_business_info(title="async_exe_script",message="script is running",data=flow_task.task_id)

            # 执行脚本
            script_result = subprocess_script_run(env_activate_command=env_activate_command
                                                ,python_interpreter=python_interpreter
                                                ,script=flow_exe_script
                                                ,dict_args=params)
            
            logs_tool.log_business_info(title="async_exe_script",message="script is runned",data=flow_task.task_id)

            # 构建回执对象
            result = res_to_FlowTaskExeResDTO(req=flow_task,res=script_result)

            # robot log report
            current_task_id = dispatch_task_core.get_current_task_id()
            dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.INFO.value[1],message='robot exec ended,release task is ' + str(current_task_id),current_task_id=current_task_id)
            
            # remove task id
            dispatch_task_core.release_current_task()
            
            # send result
            requests.post(callback_url, json=request_tool.request_base_model_json_builder(result))

            # heartbeat inmediate
            dispatch_task_core.agent_heartbeat()

        except Exception as e:
            # add log
            logs_tool.log_script_error(title="async_exe_script",message="async_exe_script run error",data=None,exc_info=e)
            
            # remove task id
            current_task_id = dispatch_task_core.get_current_task_id()
            dispatch_task_core.release_current_task()
            
            # heartbeat inmediate
            dispatch_task_core.agent_heartbeat()

            # robot log report
            dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.DEBUG.value[1],message='robot exec error , current task is ' + str(current_task_id) + '; message: ' + str(e),current_task_id=current_task_id)
            

        