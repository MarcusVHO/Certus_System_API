# Respnsavel pela lógica relacionada a usuários.

# ---------------- Imports Externos ----------------
import bcrypt
from fastapi import HTTPException
# ---------------- Imports Externos ----------------

# ---------------- Imports Internas ----------------
from src.services.security.user_service import register_new_user_in_db, find_user_in_db
# ---------------- Imports Internas ----------------


#Obs importante a funcao dever ser alterada com um middaware de permissão para manter a segurança

#Registra novo usuário
async def register_new_user(username:str, oneid:int, password:str, role:str) -> dict:
    password = hash_password(password)

    user_exist = await check_user_exists(oneid)
    if user_exist:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:
        user_data = await insert_user(username, oneid, password, role)
        return {"sucess":True, "detail":"Usuário criado com sucesso", "data":user_data}
    

#encripta senha
def hash_password(password:str) -> str:
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return password

#checa se usuário existe
async def check_user_exists(oneid: int) -> bool:
    user = await find_user_in_db(oneid)
    return bool(user)

#inseri novo usuário no banco de dados
async def insert_user(username:str, oneid:int, password:str, role:str) -> dict:
    await register_new_user_in_db(username, oneid, password, role)
    return {"oneid":oneid, "username":username}