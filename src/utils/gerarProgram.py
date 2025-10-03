from datetime import timedelta
from fastapi import HTTPException
import pandas as pd

from src.db.database import get_connection

async def gerarProgram(arquivo):
    try:
        print(arquivo)
        
        tabela = pd.read_excel(arquivo, engine='openpyxl', header=[3, 4])
        tabelaData = pd.read_excel(arquivo, header=0)

        #esssa parte pega a data
        dataProg = tabelaData.fillna(method="ffill")
        dataProg = dataProg.iloc[1]
        dataProg = dataProg.dropna().iloc[1]
        dataProg = dataProg.date()
        tabela.dropna(how='all', inplace=True)

        colunasFiltradasNormal = tabela[["Normal", "OP"]]
        colunasFiltradasSts = tabela[[("STS", "Batch/Mist."), ("STS", "OP")]]

        seq = 0
        horario = timedelta(hours=6, minutes=20)
        blocos = [[], [], [], []]  
        blocoAtual = []
        antecipa = 0
        posicao_bloco = 0
        
        # Itera sobre as linhas do DataFrame
        for index, item in colunasFiltradasNormal.iterrows():
            if item["Normal"][0] == 0:
                # print("item ignorado")
                if blocoAtual:
                    # print(f"{len(blocoAtual)} adicionado na bosicao {posicao_bloco}")
                    blocos.insert(posicao_bloco, blocoAtual)
                    blocoAtual = []
                    antecipa = 1
                    posicao_bloco = 1
            else:
                batchMist = item["Normal"][0].replace("Rotary", "").strip()
                seq += 1
                batch = batchMist.split(" - ")[0]
                mist = batchMist.split(" - ")[1]
                op = int(item["OP"][0])
                horario = horario + timedelta(minutes=30)
                hora_str = f"{horario.seconds//3600:02d}:{(horario.seconds%3600)//60:02d}"
                

                blocoAtual.append((seq, batch, mist, hora_str, op, antecipa))

                # print(f"SEQ: {seq}, BATCH: {batch}, MIST: {mist}, HORARIO:{horario}, OP: {op}, ANTECIPA: {antecipa}")

   
        horario = timedelta(hours=5, minutes=20)
        antecipa = 0
        posicao_bloco = 2
        for idex, item in colunasFiltradasSts.iterrows():

            if pd.isna(item.iloc[1]):
                # print("sts ignorado")
                
                #reseta adicona a lista de blocos e resta blocoatual
                if blocoAtual:
                    # print(f"{len(blocoAtual)} adicionado na bosicao {posicao_bloco}")
                    blocos.insert(posicao_bloco, blocoAtual)
                    blocoAtual = []
                    antecipa = 1
                    posicao_bloco = 3

            else:
                
                batchMist = item.iloc[0].replace("Rotary", "").strip()
                seq += 1
                batch = batchMist.split(" - ")[0]
                mist = batchMist.split(" - ")[1]
                op = int(item.iloc[1])
                horario = horario + timedelta(minutes=30)
                hora_str = f"{horario.seconds//3600:02d}:{(horario.seconds%3600)//60:02d}"

                #adiciona item ao bloco atula
                blocoAtual.append((seq, batch, mist, hora_str, op, antecipa))
                # print(f"STS SEQ: {seq}, BATCH: {batch}, MIST: {mist}, HORARIO:{horario}, OP: {op}, ANTECIPA: {antecipa}")
                


                




      

    except Exception as e:
        print("Erro ao ler o arquivo:", e)



    
    print(f"Data Program: {dataProg} Normais: {len(blocos[0])}, Normais Antecipa: {len(blocos[1])}, STS: {len(blocos[2])}, STS Antecipa {len(blocos[3])}")
    return dataProg, blocos[0], blocos[1], blocos[2], blocos[3]



async def inserirProgramacaoDb(data, normais, normaisAntecipa, sts, stsAntecipa):
    
    conn = get_connection()
    data = pd.to_datetime(data).date()

    try:
        with conn.cursor() as cursor: 
            
            #verifica se dia existe antes de inserir
            cursor.execute(
                "SELECT * FROM programDays WHERE data = (%s);", (data,)
            )

            if cursor.fetchone() is None:

                cursor.execute(
                    "INSERT INTO programDays (data) VALUES (%s);",(data,)
                )
                conn.commit()

                cursor.execute(
                    "SELECT id FROM programDays WHERE data = (%s)",(data,)
                )
                
                
                id = cursor.fetchone()["id"]
                print(id)

                normais = normais + normaisAntecipa 
                normais = [t + (id,) for t in normais]
                sts = sts + stsAntecipa
                sts = [t + (id,) for t in sts]

                if normais:
                    cursor.executemany(
                        "INSERT IGNORE INTO itens_normais (seq, batch, mist, horario, op, antecipado, dia_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",normais
                    )
                
                if sts:
                    cursor.executemany(
                        "INSERT IGNORE INTO itens_sts (seq, batch, mist, horario, op, antecipado, dia_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",sts
                    )
                    conn.commit()

    
            else:
                print("Programação já existe")
                raise HTTPException(status_code=422, detail="Programação já existe!!!")

    finally:
        conn.close()

