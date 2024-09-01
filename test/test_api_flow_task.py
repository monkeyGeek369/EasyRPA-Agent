import unittest
import requests
import json


script = """
import json
from playwright import sync_api
import sys
import os

def print_json(data):
    print(json.dumps(data))

print_json({"message": "123"})

env_var1 = os.getenv('key1', 'Default Value')
print(f"{env_var1}")
env_var2 = os.getenv('key2', 'Default Value')
print(f"{env_var2}")
env_var3 = os.getenv('key3', 'Default Value')
print(f"{env_var3}")

def test():
    print_json({"len": len(sys.argv), "args": sys.argv})
print_json({"message": "456"})
test()
print_json({"message": "78\\n9"})
            """

class FlowTaskTest(unittest.TestCase):
    def test_flow_task_sync_exe(self):
        # 假设这是我们要测试的接口的URL
        url = 'http://127.0.0.1:5000/flow/task/sync/exe'
        params = {"key1":"value1","key2":"value2","key3":"123"}
        data = {
            'task_id': 123,
            'site_id': 456,
            'flow_id': 789,
            'flow_code': 'test_code',
            'flow_name': 'test_name',
            'flow_rpa_type': 1,
            'flow_exe_env': 'playwright',
            'flow_standard_message': json.dumps(params),
            'flow_exe_script': script,
            }
        response = requests.post(url, json=data)
        print(response)

if __name__ == "__main__":
    unittest.main()