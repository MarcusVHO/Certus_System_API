from datetime import timedelta
from datetime import datetime
from operator import indexOf
import sys
from dotenv import load_dotenv
import mysql
import mysql.connector
import pandas as pd
import os

def gerarProgram(arquivo):
    try:
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
        ordem = 0
        horario = timedelta(hours=6, minutes=20)
        blocos = []
        blocoAtual = []
        antecipa = 0
        
        # Itera sobre as linhas do DataFrame
        for index, item in colunasFiltradasNormal.iterrows():
            if item["Normal"][0] == 0:
                print("item ignorado")
                if blocoAtual:
                    blocos.append(blocoAtual)
                    blocoAtual = []
                    ordem = 0
                    antecipa = 1
            else:
                batchMist = item["Normal"][0].replace("Rotary", "").strip()
                seq += 1
                batch = batchMist.split(" - ")[0]
                mist = batchMist.split(" - ")[1]
                op = int(item["OP"][0])
                horario = horario + timedelta(minutes=30)
                hora_str = f"{horario.seconds//3600:02d}:{(horario.seconds%3600)//60:02d}"
                ordem += 1
                

                blocoAtual.append((seq, batch, mist, ordem, hora_str, op, antecipa))

                print(f"SEQ: {seq}, BATCH: {batch}, MIST: {mist}, ORDEM: {ordem}, HORARIO:{horario}, OP: {op}, ANTECIPA: {antecipa}")

        ignorar = 0
        horario = timedelta(hours=5, minutes=20)
        antecipa = 0

        for idex, item in colunasFiltradasSts.iterrows():

            if pd.isna(item.iloc[1]):
                print("sts ignorado")
                
                #reseta adicona a lista de blocos e resta blocoatual
                if blocoAtual:
                    blocos.append(blocoAtual)
                    blocoAtual = []
                    ordem = 0
                    antecipa = 1

            else:
                if ignorar < 3:
                    ignorar += 1
                else:
                    batchMist = item[0].replace("Rotary", "").strip()
                    seq += 1
                    batch = batchMist.split(" - ")[0]
                    mist = batchMist.split(" - ")[1]
                    op = int(item[1])
                    horario = horario + timedelta(minutes=30)
                    hora_str = f"{horario.seconds//3600:02d}:{(horario.seconds%3600)//60:02d}"
                    ordem += 1

                    #adiciona item ao bloco atula
                    blocoAtual.append((seq, batch, mist, ordem, hora_str, op, antecipa))
                    print(f"STS SEQ: {seq}, BATCH: {batch}, MIST: {mist}, ORDEM: {ordem}, HORARIO:{horario}, OP: {op}, ANTECIPA: {antecipa}")
                    


                




      
        print(f"Data Program: {dataProg} Normais: {blocos[0]}, Normais Antecipa: {blocos[1]}, STS: {blocos[2]}, STS Antecipa {blocos[3]}")

    except Exception as e:
        print("Erro ao ler o arquivo:", e)

    return dataProg, blocos[0], blocos[1], blocos[2], blocos[3]



def inserirProgramacaoDb(data, normais, normaisAntecipa, sts, stsAntecipa):
    load_dotenv()
    
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    database = "CERTUS"

    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor(buffered=True)

    cursor.execute(
        "INSERT INTO programDays (data) VALUES (%s);",(data,)
    )
    conn.commit()

    cursor.execute(
        "SELECT id FROM programDays WHERE data = %s",(data,)
    )

    id = cursor.fetchone()[0]


    normais = normais + normaisAntecipa 
    normais = [t + (id,) for t in normais]
    sts = sts + stsAntecipa
    sts = [t + (id,) for t in sts]

    cursor.executemany(
        "INSERT INTO itens_normais (seq, batch, mist, ordem, horario, op, antecipado, dia_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",normais
    )
    conn.commit()

    cursor.executemany(
        "INSERT INTO itens_sts (seq, batch, mist, ordem, horario, op, antecipado, dia_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",sts
    )
    conn.commit()
    
    conn.commit()
    cursor.close()

    print(normais)


if __name__ == "__main__":
    if len(sys.argv)<2:
        print("informe o caminho do aruivo Excel")
        sys.exit(1)
    data, normais, normaisAntecipa, sts, stsAntecipa = gerarProgram(sys.argv[1])
    inserirProgramacaoDb(data, normais, normaisAntecipa, sts, stsAntecipa)
