from flask import Flask
from agent_api import agent_core_bp
from agent_api import flow_task_bp

# 注册flask应用
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(agent_core_bp)
app.register_blueprint(flow_task_bp)