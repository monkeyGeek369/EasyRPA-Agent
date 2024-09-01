from typing import List
class FlowTaskExeResDTO:
    def __init__(self
                 ,task_id:int,site_id:int
                 ,flow_id:int,flow_code:str,flow_name:str,flow_rpa_type:int
                 ,flow_exe_env:str
                 ,status:bool
                 ,error_msg:str
                 ,print_str:List[str]
                 ,result:str):
        self.task_id = task_id
        self.site_id = site_id
        self.flow_id = flow_id
        self.flow_code = flow_code
        self.flow_name = flow_name
        self.flow_rpa_type = flow_rpa_type
        self.flow_exe_env = flow_exe_env
        self.status = status
        self.error_msg = error_msg
        self.print_str = print_str
        self.result = result
        
    def to_dict(self):
        return self.__dict__