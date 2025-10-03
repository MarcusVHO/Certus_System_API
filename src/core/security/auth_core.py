# responsavel por logica de authenticação

# ---------------- Imports Externos ----------------
from datetime import datetime, timedelta
import os
import bcrypt
from fastapi import HTTPException, Response
import jwt
# ---------------- Imports Externos ----------------

# ---------------- Imports Internos ----------------
from src.services.security.auth_service import get_refresh_token_in_db_by_id, insert_refresh_token_in_db
from src.core.security.user_core import check_user_exists
from src.services.security.user_service import find_user_in_db
# ---------------- Imports Internos ----------------


#Loga usuário no sistema
async def user_login(oneid:int, password:str, response: Response)->dict:
    
    user_exist = await check_user_exists(oneid)

    if not user_exist:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        user_data = await get_user_data(oneid)

        password_validation = password_compare(password, user_data["password"])
        print(password_validation)
        if password_validation:
            access_token, refres_token = get_tokens(user_data)

            response.set_cookie(
                key="refresh_token",
                value=refres_token,
                httponly=True,
                samesite="strict",
                max_age=480*60
            )
            await insert_refresh_token_in_db(refres_token, user_data["id"])

            return {"sucess":True, "detail":"Usuário logado com sucesso", "access_token":access_token}
        else:
            raise HTTPException(status_code=401, detail="Senha incorreta")


#obtem informações do usuário
async def get_user_data(oneid:int = None, id:int = None)->dict:
    user_data = await find_user_in_db(oneid,id)
    return user_data


#compara senhas
def password_compare(password_input:str, password_db:str)->bool:
    if bcrypt.checkpw(password_input.encode("utf-8"), password_db.encode("utf-8")):
        return True
    else:
        return False
    

#obtem tokens de authenticação
def get_tokens(data:dict, expire:int = 30, expire_refresh:int = 480)->tuple[str, str]:
    payload_access = data.copy()
    payload_access.pop("password", None)
    secret = os.getenv("SECRET")
    secret_refresh_token = os.getenv("REFRESH_TOKEN_SECRET")
    algorithm = os.getenv("ALGORITHM")

    exp = datetime.utcnow() + timedelta(minutes=expire) 
    exp_refresh_token = datetime.utcnow() + timedelta(minutes=expire_refresh) 
    payload_access["exp"] = int(exp.timestamp())

    payload_refresh_token = {
        "id": payload_access["id"],
        "exp": int(exp_refresh_token.timestamp())
    }

    token = jwt.encode(payload_access, secret, algorithm=algorithm)
    refresh_token = jwt.encode(payload_refresh_token, secret_refresh_token, algorithm=algorithm)

    return token, refresh_token


#Obtem novos tokens através do refresh token 
async def get_new_tokens(refresh_token:str, response: Response)->dict:
    try:
        algorithm = os.getenv("ALGORITHM")
        secret_refresh_token = os.getenv("REFRESH_TOKEN_SECRET")
      
        payload = jwt.decode(refresh_token, secret_refresh_token, algorithms=algorithm)
        token_from_db = await get_refresh_token_in_db_by_id(payload["id"])

        print("Informações do refresh token", payload)

        if refresh_token == token_from_db["refresh_token"]:
            user_data = await get_user_data(None, payload["id"])
            access_token, refres_token = get_tokens(user_data)
            
            response.set_cookie(
                    key="refresh_token",
                    value=refres_token,
                    httponly=True,
                    samesite="strict",
                    max_age=480*60
                )
            

            await insert_refresh_token_in_db(refres_token, user_data["id"])

            return {"sucess":True, "detail":"Novos tokens concedidos com sucesso", "access_token":access_token}
        else:
            raise HTTPException(status_code=401, detail="Token invalido")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido")

