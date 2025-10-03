# responsavel por logica de da programçao
# ---------------- Imports Externos ----------------
from fastapi import Path
# ---------------- Imports Externos ----------------
# ---------------- Imports Internos ----------------

from src.services.pmd.programacao_service import get_list_programacoes, get_programacao_data_in_db
from src.utils.gerarProgram import gerarProgram, inserirProgramacaoDb
# ---------------- Imports Internos ----------------



#obtem programacoes
async def get_programacoes(data1:str, data2:str)->dict:
    programacoes = await get_list_programacoes(data1, data2)
    print(programacoes)
    return programacoes

#adiciona nivel programacao
async def add_new_programacao(data:Path)->dict:
        arquivo = await data.read()
        data, normais, normaisAntecipa, sts, stsAntecipa = await gerarProgram(arquivo)
        await inserirProgramacaoDb(data, normais, normaisAntecipa, sts, stsAntecipa)
        return({'sucess': True})

#obtem os dados de um programação especifica
async def get_programacao_data_core(id:int)->tuple:
    data = await get_programacao_data_in_db(id)
    return(data)
    
    
    