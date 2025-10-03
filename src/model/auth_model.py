
from pydantic import BaseModel, field_validator


class login(BaseModel):
    oneid: int
    password: str

    @field_validator("oneid")
    def validation_oneid(cls, v):
        if len(str(v)) == 8:
            return v
        else:
            raise ValueError("Oneid deve ter 8 dígitos")
