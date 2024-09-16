from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
import jsonpickle

def req_to_FlowTaskExeReqDTO(req_json:str) -> FlowTaskExeReqDTO:
    dto = jsonpickle.decode(req_json)
    if dto is None:
        return None
    return dto.model
