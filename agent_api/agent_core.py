from flask import jsonify,Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper

agent_core_bp =  Blueprint('agent_core',__name__)

@agent_core_bp.route('/health/test', methods=['GET'])
@easyrpa_request_wrapper
def health_test():
    return jsonify({'message': 'Healthy!'})