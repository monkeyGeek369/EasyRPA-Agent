from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.json_tools import JsonTool
from core import dispatch_task_core

agent_core_bp =  Blueprint('agent_core',__name__)

@agent_core_bp.route('/health/test', methods=['GET'])
@easyrpa_request_wrapper
def health_test(params):
    return JsonTool.any_to_dict({'message': 'Healthy!'})

@agent_core_bp.route('/release/agent', methods=['GET'])
@easyrpa_request_wrapper
def release_agent(params):
    dispatch_task_core.release_current_task()
    return JsonTool.any_to_dict({'message': 'Released!'})