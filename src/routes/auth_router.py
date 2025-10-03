# Responsavel por gerenciar rotas de autenticação

# ---------------- Imports Externos ----------------
from fastapi import APIRouter, HTTPException, Request, Response

from src.core.security.auth_core import get_new_tokens, user_login
from src.model.auth_model import login
import traceback
# ---------------- Imports Externos ----------------

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
async def welcome():
    return {"message": "Bem vindo a rota de authenticação"}

@router.post("/login")
async def login(user_information: login, response: Response):
    try:
        result = await user_login(user_information.oneid, user_information.password, response)
        return result
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
 


@router.get("/refresh_token")
async def refresh_token(request: Request, response: Response):
    try:
        result = await get_new_tokens(request.cookies["refresh_token"], response)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
        