from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.json_tools import JsonTool
from easyrpa.tools import request_tool,local_store_tools,logs_tool
from core import dispatch_task_core

agent_core_bp =  Blueprint('agent_core',__name__)

@agent_core_bp.route('/health/test', methods=['GET'])
@easyrpa_request_wrapper
def health_test(params):
    return JsonTool.any_to_dict({'message': 'Healthy!'})

@agent_core_bp.route('/release/agent', methods=['GET'])
@easyrpa_request_wrapper
def release_agent(params):
    local_store_tools.delete_data("task_id")
    return JsonTool.any_to_dict({'message': 'Released!'})