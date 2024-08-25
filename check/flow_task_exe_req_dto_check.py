import agent_models.req.flow_task_exe_req_dto as task_dto

def base_check(dto:task_dto):
    if dto is None:
        return todo