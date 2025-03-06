from easyrpa.script_exe import sync_python_script
from transfer.flow_task_exe_res_dto_transfer import res_to_FlowTaskExeResDTO
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.models.flow.flow_script_search_dto import FlowScriptSearchDTO
from easyrpa.enums.sys_log_type_enum import SysLogTypeEnum
from easyrpa.enums.script_type_enum import ScriptTypeEnum
from core import dispatch_task_core
import requests,os
from easyrpa.tools import request_tool,logs_tool


def get_project_root_path() -> str:
    project_root = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(project_root, 'setup.py')) and not os.path.isfile(os.path.join(project_root, 'requirements.txt')):
        if project_root == os.path.dirname(project_root):
            project_root = None
            break
        project_root = os.path.dirname(project_root)
    return project_root

class ScriptExeCore:
    def async_exe_script(self,flow_task:FlowTaskExeReqDTO,params,callback_url:str,script_url:str):
        try:
            logs_tool.log_business_info(title="async_exe_script",message="script is running",data=flow_task.task_id)

            # check script is exist
            project_root = get_project_root_path()
            is_exist = sync_python_script.script_is_exist(flow_code=flow_task.flow_code,script_type=ScriptTypeEnum.EXECUTION.value[0],script_hash=flow_task.script_hash,project_root=project_root)

            # if not exist, create script file
            if not is_exist:
                logs_tool.log_business_info(title="async_exe_script",message="script is creating",data=flow_task.task_id)
                # get script
                script_search_params = FlowScriptSearchDTO(
                    flow_code=flow_task.flow_code,
                    script_type=ScriptTypeEnum.EXECUTION.value[0]
                )
                script = None
                script_response = requests.post(script_url, json=request_tool.request_base_model_json_builder(script_search_params))
                if script_response is not None and script_response.status_code == 200:
                    result_txt = logs_tool.JsonTool.any_to_dict(script_response.text)
                    if result_txt.get("code") == 200 and result_txt.get("data") is not None:
                        script_response_data = logs_tool.JsonTool.any_to_dict(result_txt.get("data"))
                        if script_response_data is not None and script_response_data.get("script") is not None:
                            script = script_response_data.get("script")
                
                if script is None:
                    raise EasyRpaException("get flow exe script failed",EasyRpaExceptionCodeEnum.DATA_NULL,None,flow_task)
                # create script file
                sync_python_script.create_script_file(flow_code=flow_task.flow_code,script_type=ScriptTypeEnum.EXECUTION.value[0],script_hash=flow_task.script_hash,script=script,project_root=project_root)
                logs_tool.log_business_info(title="async_exe_script",message="script is created",data=flow_task.task_id)

            # script exe
            script_result = sync_python_script.sync_script_run(flow_code=flow_task.flow_code,script_type=ScriptTypeEnum.EXECUTION.value[0],script_hash=flow_task.script_hash,params=params,project_root=project_root)
            logs_tool.log_business_info(title="async_exe_script",message="script is runned",data=flow_task.task_id)

            # build result
            result = res_to_FlowTaskExeResDTO(req=flow_task,res=script_result)

            # robot log report
            current_task_id = dispatch_task_core.get_current_task_id()
            dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.INFO.value[1],message='robot exec ended,release task is ' + str(current_task_id),current_task_id=current_task_id)
            
            # remove task id
            dispatch_task_core.release_current_task()
            
            # heartbeat inmediate
            dispatch_task_core.agent_heartbeat()

            # send result
            requests.post(callback_url, json=request_tool.request_base_model_json_builder(result))

        except Exception as e:
            logs_tool.log_script_info(title="async_exe_script",message="async_exe_script run error , record start",data=None)
            
            # remove task id
            current_task_id = dispatch_task_core.get_current_task_id()
            dispatch_task_core.release_current_task()
            
            # heartbeat inmediate
            dispatch_task_core.agent_heartbeat()

            # robot log report
            error_info = safe_exception_to_string(e)
            dispatch_task_core.robot_log_report_handler(log_type=SysLogTypeEnum.DEBUG.value[1],message='robot exec error , current task is ' + str(current_task_id) + '; message: ' + error_info,current_task_id=current_task_id)
            
            # add log
            logs_tool.log_script_error(title="async_exe_script",message="async_exe_script run error",data=None,exc_info=e)
            
def safe_exception_to_string(e) -> str:
    """
    将异常对象 e 安全地转换为字符串，即使其内部实现有缺陷或参数无法转换。
    保证在任何情况下不会抛出异常。
    """
    default_msg = "Unknown error"
    
    if e is None:
        return default_msg
    
    # 第一步：尝试直接调用 str(e)
    try:
        return str(e)
    except Exception:
        pass
    
    # 第二步：尝试获取异常类型和参数
    try:
        exc_type = e.__class__.__name__
    except AttributeError:
        exc_type = "UnknownException"
    
    # 第三步：安全处理异常参数 (e.args)
    try:
        args = e.args
    except AttributeError:
        args = ()
    
    arg_strings = []
    for arg in args:
        try:
            arg_str = str(arg)
        except Exception:
            arg_str = "<无法转换的参数>"
        arg_strings.append(arg_str)
    
    # 组合信息
    if arg_strings:
        return f"{exc_type}: {', '.join(arg_strings)}"
    else:
        return exc_type
        