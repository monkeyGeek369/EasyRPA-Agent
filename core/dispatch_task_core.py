from easyrpa.models.agent_models.heartbeat_check_req_dto import HeartbeatCheckReqDTO
from easyrpa.tools import request_tool,local_store_tools,machine_tools,logs_tool
from easyrpa.models.agent_models.robot_log_report_req_dto import RobotLogReportReqDTO
from configuration import app_config
import requests

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
    # get url
    control_url = app_config.EASYRPA_URL
    api_pash = app_config.HEART_BEAT_CHECK_API
    url = control_url + api_pash

    # build params
    data = HeartbeatCheckReqDTO(
        robot_code=build_robot_code(),
        robot_ip=get_robot_ip(),
        port= app_config.ROBOT_SERVER_PORT,
        task_id=local_store_tools.get_data("task_id")
    )

    # report
    requests.post(url, json=request_tool.request_base_model_json_builder(data))

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