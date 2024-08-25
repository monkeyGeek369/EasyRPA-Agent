
# 从请求中获取指定内容
def get_parameter(request, param, default, cast_type):
    #  先request.args 后request.form 然后转换cast_type=int|float类型。
    for method in [request.args.get, request.form.get]:
        value = method(param, "").strip()
        if value:
            try:
                return cast_type(value)
            except ValueError:
                break  # args转换失败，退出尝试form
    return default  # 失败，返回默认值。
