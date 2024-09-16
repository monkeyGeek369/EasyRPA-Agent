from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.models.scripty_exe_result import ScriptExeResult

def res_to_FlowTaskExeResDTO(req:FlowTaskExeReqDTO,res:ScriptExeResult) -> FlowTaskExeResDTO:
    return FlowTaskExeResDTO(
        task_id = req.task_id,
        site_id = req.site_id,
        flow_id = req.flow_id,
        flow_code = req.flow_code,
        flow_name = req.flow_name,
        flow_rpa_type = req.flow_rpa_type,
        flow_exe_env = req.flow_exe_env,
        sub_source=req.sub_source,
        status = res.status,
        error_msg = res.error_msg,
        print_str = res.print_str,
        result = res.result,
        code=res.code
        )