# Responsavel por gerenciar rotas do pmd

# ---------------- Imports Externos ----------------
from fastapi import APIRouter, HTTPException, UploadFile
# ---------------- Imports Externos ----------------

# ---------------- Imports Internos ----------------
from src.core.pmd.programacao_core import add_new_programacao, get_programacao_data_core, get_programacoes
from src.model.get_programacao_model import get_new_programacao, get_prog_data_model
# ---------------- Imports Internos ----------------




router = APIRouter(prefix="/pmd", tags=["pmd"])



#Apenas testa a rota
@router.get("/")
async def welcome():
    return {"message": "Bem vindo a rota do PMD"}


@router.post("/get_programacao")
async def get_programacao(data: get_new_programacao):
    try:
        print(f"Buscando programação de {data.data1} à {data.data2}")
        response = await get_programacoes(data.data1, data.data2)
        return response

    #Trata possiveis erros no código
    except HTTPException:
        raise
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
    

@router.post("/add_new_programacao")
async def add_new_programtion(xlsx_file: UploadFile):
    try:
        print("Criando programação....")
        response = await add_new_programacao(xlsx_file)

        return response
    except HTTPException:
        raise
    except Exception as e:
         print(e)
         raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
    
@router.post("/get_programacao_data")
async def get_programacao_data(data: get_prog_data_model):
    try:
        response = await get_programacao_data_core(data.id, data.type)
        return response
    except HTTPException:
        raise
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Erro interno: {e}")