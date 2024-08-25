
class FlowTaskExeReqDTO:
    def __init__(self
                 ,task_id:int,site_id:int
                 ,flow_id:int,flow_code:str,flow_name:str,flow_rpa_type:int
                 ,flow_exe_env:str
                 ,flow_standard_message:str
                 ,flow_exe_script:str):
        self.task_id = task_id
        self.site_id = site_id
        self.flow_id = flow_id
        self.flow_code = flow_code
        self.flow_name = flow_name
        self.flow_rpa_type = flow_rpa_type
        self.flow_exe_env = flow_exe_env
        self.flow_standard_message = flow_standard_message
        self.flow_exe_script = flow_exe_script