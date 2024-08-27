from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.PrintCollector import PrintCollector


# 用户提交的代码，这段代码将访问外部传入的参数 `external_data`
user_code = """
def process_data(data):
    return data

# 假设我们期望的外部数据是一个字符串
result = process_data(external_data)
"""

# 准备要传递给用户代码的外部参数数据
external_data = {"key":"value","key2":123,"key3":False}
# 创建受限的全局变量字典，包括 safe_builtins 和外部参数
my_safe_builtins = safe_builtins.copy()
restricted_globals = {
    "__builtins__": my_safe_builtins,
    "_print_":PrintCollector,
    '_getattr_': getattr,
    "external_data": external_data  # 添加外部参数到全局变量字典
}

# 编译用户代码为受限代码
bytecode = compile_restricted(user_code, "<string>", "exec")

# 执行编译后的代码，使用受限的全局变量字典
try:
    exec(bytecode, restricted_globals)
    # 如果需要获取用户代码中的变量，例如 result
    print("Result from user code:", restricted_globals['result'])
except Exception as e:
    print("Error during code execution:", e)