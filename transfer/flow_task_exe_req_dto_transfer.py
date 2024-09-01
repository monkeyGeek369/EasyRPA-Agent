from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO

def req_to_FlowTaskExeReqDTO(req_json):
    dto = FlowTaskExeReqDTO(**req_json)
    return dto
