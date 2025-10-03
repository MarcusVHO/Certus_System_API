# responsavel pelas rotas de usuário

# ---------------- Imports Externos ----------------
from fastapi import APIRouter, HTTPException
# ---------------- Imports Externos ----------------

# ---------------- Imports Internos ----------------
from src.core.security.user_core import register_new_user
from src.model.user_model import new_user
# ---------------- Imports Internos ----------------

router = APIRouter(prefix="/user", tags=["user"])


#Apenas testa a rota
@router.get("/")
async def welcome():
    return {"message": "Bem vindo a rota de usuários"}

# Responsavel por registrar novos usuários
@router.post("/register")
async def register_user(new_user: new_user):
    try: 
        response = await register_new_user(new_user.username, new_user.oneid, new_user.password, new_user.role)
        return response #retorna a resposta do registro
    
    #Trata possiveis erros no código
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")