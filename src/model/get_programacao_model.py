
from pydantic import BaseModel

class get_new_programacao(BaseModel):
    data1: str
    data2: str
  
    
class get_prog_data_model(BaseModel):
    id: int