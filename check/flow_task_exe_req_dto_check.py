import agent_models.req.flow_task_exe_req_dto as task_dto
from easyrpa.models.easy_rpa_exception import EasyRpaException

def base_check(dto:task_dto):
    if dto is None:
        raise EasyRpaException("",)
        return todo