import agent_models.req.flow_task_exe_req_dto as task_req

def req_to_FlowTaskExeReqDTO(req_json):
    dto = task_req.FlowTaskExeReqDTO(**req_json)
    return dto
