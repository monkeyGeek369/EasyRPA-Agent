from flask import jsonify,Blueprint,request
from transfer import flow_task_exe_req_dto_transfer
from check import flow_task_exe_req_dto_check 


flow_task_bp =  Blueprint('flow_task',__name__)

# 流程任务执行接口
@flow_task_bp.route('/flow/task/exe', methods=['POST'])
def flow_task_exe():
    # 获取请求对象
    req_json = request.get_json
    flow_task = flow_task_exe_req_dto_transfer.req_to_FlowTaskExeReqDTO(req_json)

    # 校验请求对象
    flow_task_exe_req_dto_check.base_check(flow_task)

    return jsonify({'message': 'Hello, World!'})