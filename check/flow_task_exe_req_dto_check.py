from agent_models.req.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import str_tools,number_tool

def base_check(dto:FlowTaskExeReqDTO):
    if dto is None:
        raise EasyRpaException("请求参数为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if number_tool.num_is_empty(dto.task_id):
        raise EasyRpaException("任务id为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if number_tool.num_is_empty(dto.site_id):
        raise EasyRpaException("站点id为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if number_tool.num_is_empty(dto.flow_id):
        raise EasyRpaException("流程id为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if str_tools.str_is_empty(dto.flow_code):
        raise EasyRpaException("流程code为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if str_tools.str_is_empty(dto.flow_name):
        raise EasyRpaException("流程name为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if number_tool.num_is_empty(dto.flow_rpa_type):
        raise EasyRpaException("流程rpa类型为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if str_tools.str_is_empty(dto.flow_exe_env):
        raise EasyRpaException("流程执行环境为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if str_tools.str_is_empty(dto.flow_standard_message):
        raise EasyRpaException("流程标准消息",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if str_tools.str_is_empty(dto.flow_exe_script):
        raise EasyRpaException("流程执行脚本为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)