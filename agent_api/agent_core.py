from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.json_tools import JsonTool

agent_core_bp =  Blueprint('agent_core',__name__)

@agent_core_bp.route('/health/test', methods=['GET'])
@easyrpa_request_wrapper
def health_test(params):
    return JsonTool.any_to_dict({'message': 'Healthy!'})