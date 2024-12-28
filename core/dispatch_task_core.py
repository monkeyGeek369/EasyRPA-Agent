from easyrpa.models.agent_models.heartbeat_check_req_dto import HeartbeatCheckReqDTO
from easyrpa.tools import request_tool,local_store_tools,machine_tools,logs_tool
from easyrpa.models.agent_models.robot_log_report_req_dto import RobotLogReportReqDTO
from configuration import app_config
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from easyrpa.enums.rpa_exe_result_code_enum import RpaExeResultCodeEnum
import requests,datetime

def heartbeat_check_handler(params):
    while True:
        try:
            agent_heartbeat()
            
            # gren 10-20s
            import random
            wait_time = random.uniform(10, 20)

            # wait 10-20s
            import time
            time.sleep(wait_time)
        except Exception as e:
            logs_tool.log_business_error(title="heartbeat_check_handler",message="heartbeat error",data=str(e),exc_info=e)


def agent_heartbeat():
    try:
        control_url = app_config.EASYRPA_URL

        # check current is expired
        if current_task_is_expired():
            # get control url
            result_pash = app_config.TASK_RESULT_PUSH_API
            result_url = control_url + result_pash
            data = get_current_task()
            # build params
            result_parms = FlowTaskExeResDTO(
            task_id = data.task_id,
            site_id = data.site_id,
            flow_id = data.flow_id,
            flow_code = data.flow_code,
            flow_name = data.flow_name,
            flow_rpa_type = data.flow_rpa_type,
            flow_exe_env = data.flow_exe_env,
            sub_source=data.sub_source,
            status = False,
            error_msg = "task is expired , robot delete task",
            print_str = None,
            result = "task is expired , robot delete task",
            code=RpaExeResultCodeEnum.FLOW_EXE_ERROR.value[1]
            )
            # report
            requests.post(result_url, json=request_tool.request_base_model_json_builder(result_parms))

        # get url
        api_pash = app_config.HEART_BEAT_CHECK_API
        url = control_url + api_pash

        # build params
        data = HeartbeatCheckReqDTO(
            robot_code=build_robot_code(),
            robot_ip=get_robot_ip(),
            port= app_config.ROBOT_SERVER_PORT,
            task_id=get_current_task_id()
        )

        # report
        requests.post(url, json=request_tool.request_base_model_json_builder(data))
    except Exception as e:
        logs_tool.log_business_error(title="heartbeat_check_handler",message="heartbeat error",data=str(e),exc_info=e)

def build_robot_code() -> str:
    args = []
    # get mac
    mac = machine_tools.get_machine_mac_id()
    if mac is not None:
        args.append(mac)

    # get cpu
    cpu = machine_tools.get_machine_cpu_id()
    if cpu is not None:
        args.append(cpu)

    # get disk id
    disk = machine_tools.get_machine_disk_id()
    if disk is not None:
        args.append(disk)

    # get board id
    board = machine_tools.get_main_board_id()
    if board is not None:
        args.append(board)

    return machine_tools.get_machine_id(salt="easyrpa_robot", key="code", args=args)

def get_robot_ip() -> str:
    ip = app_config.ROBOT_DEFAULT_IP
    if ip is not None:
        return ip

    # get ips
    ips = machine_tools.get_machine_ips()
    if ips is not None:
        return ips[0]
    return None
    

def robot_log_report_handler(log_type:int,message:str,current_task_id:int):
    try:
        # build params
        params = RobotLogReportReqDTO(
            robot_code=build_robot_code(),
            task_id=current_task_id,
            log_type=log_type,
            message=message
        )

        # get url
        control_url = app_config.EASYRPA_URL
        api_pash = app_config.ROBOT_LOG_REPORT_API
        url = control_url + api_pash

        # report
        requests.post(url, json=request_tool.request_base_model_json_builder(params))
    except Exception as e:
        logs_tool.log_business_error(title="robot_log_report_handler",message="robot log report error",data=current_task_id,exc_info=e)

def set_current_task(req:FlowTaskExeReqDTO):
    data = {}
    data["task_info"] = req
    data["max_exe_time"] = req.max_exe_time
    data["set_time"] = datetime.datetime.now().timestamp()
    local_store_tools.add_data("current_task", data)

def release_current_task():
    local_store_tools.delete_data("current_task")

def get_current_task_id() -> int:
    data = local_store_tools.get_data("current_task")
    if data is not None:
        info = data.get("task_info")
        if info is not None:
            return info.task_id
    return None

def current_task_is_expired() -> bool:
    data = local_store_tools.get_data("current_task")
    if data is not None:
        if datetime.datetime.now().timestamp() - data.get("set_time") > data.get("max_exe_time"):
            return True
    return False

def get_current_task() -> FlowTaskExeReqDTO:
    data = local_store_tools.get_data("current_task")
    if data is not None:
        return data.get("task_info")
    return None
