from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.tools.json_tools import JsonTool

def req_to_FlowTaskExeReqDTO(req_json:str) -> FlowTaskExeReqDTO:
    dto = JsonTool.any_to_dict(req_json)
    if dto is None:
        return None
    model = dto.get("model")

    ret = FlowTaskExeReqDTO(
        task_id=model.get("task_id"),
        site_id=model.get("site_id"),
        flow_id=model.get("flow_id"),
        flow_code=model.get("flow_code"),
        flow_name=model.get("flow_name"),
        flow_rpa_type=model.get("flow_rpa_type"),
        flow_exe_env=model.get("flow_exe_env"),
        flow_standard_message=model.get("flow_standard_message"),
        flow_exe_script=model.get("flow_exe_script"),
        sub_source=model.get("sub_source")
    )
    return ret
