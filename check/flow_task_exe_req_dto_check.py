from agent_models.req.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum

def base_check(dto:FlowTaskExeReqDTO):
    if dto is None:
        raise EasyRpaException("请求参数为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.task_id is None:
        raise EasyRpaException("任务id为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.site_id is None:
        raise EasyRpaException("站点id为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.flow_id is None:
        raise EasyRpaException("流程id为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.flow_code is None:
        raise EasyRpaException("流程code为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.flow_name is None:
        raise EasyRpaException("流程name为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.flow_rpa_type is None:
        raise EasyRpaException("流程rpa类型为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.flow_exe_env is None:
        raise EasyRpaException("流程执行环境为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.flow_standard_message is None:
        raise EasyRpaException("流程标准消息",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)
    if dto.flow_exe_script is None:
        raise EasyRpaException("流程执行脚本为空",EasyRpaExceptionCodeEnum.DATA_NULL.code,None,dto)