from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import str_tools,number_tool

def base_check(dto:FlowTaskExeReqDTO):
    if number_tool.num_is_empty(dto.task_id):
        raise EasyRpaException("task id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.site_id):
        raise EasyRpaException("site id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.flow_id):
        raise EasyRpaException("flow id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_tools.str_is_empty(dto.flow_code):
        raise EasyRpaException("flow code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_tools.str_is_empty(dto.flow_name):
        raise EasyRpaException("flow name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.flow_rpa_type):
        raise EasyRpaException("rpa type is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_tools.str_is_empty(dto.script_hash):
        raise EasyRpaException("script hash is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_tools.str_is_empty(dto.flow_standard_message):
        raise EasyRpaException("flow standard message is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)