from pydantic import BaseModel, field_validator

class new_user(BaseModel):
    username: str
    oneid: int
    password: str
    confirm_password: str
    role: str
    

    @field_validator("oneid")
    def validate_oneid(cls, v):
        if len(str(v)) != 8:
            raise ValueError("Oneid deve ter 8 dígitos")
        return v
    
    @field_validator("confirm_password")
    def password_confirmation(cls, v, info):
        password = info.data.get("password")
        if password and v != password:
            raise ValueError("As senhas não conferem")
        return v 
        
    @field_validator("role")
    def role_validation(cls, v, info):
        if v in ["owner", "admin", "manager", "user"]:
            return v
        else:
            raise ValueError("Authorização de usuário invalida")