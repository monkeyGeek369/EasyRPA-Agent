from flask import jsonify,Blueprint

agent_core_bp =  Blueprint('agent_core',__name__)

@agent_core_bp.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, World!'})