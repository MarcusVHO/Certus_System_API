#Responsavel pela comunicação com serviços para funcoes relacionadas a programacao

# ---------------- Imports Externos ----------------
# ---------------- Imports Externos ----------------

# ---------------- Imports Internas ----------------
from src.db.database import get_connection
# ---------------- Imports Internas ----------------


#responsavel por achar os itens da programacao
async def get_list_programacoes(data1, data2):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT * FROM programDays WHERE DATE(data) BETWEEN %s AND %s ORDER BY data ASC;
            """, (data1, data2))

            response = cursor.fetchall()
            return response

    finally:
        conn.close()

async def get_programacao_data_in_db(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT * FROM (
                SELECT *,"Normal" as tipo  FROM itens_normais WHERE dia_id = %s
                UNION ALL
                SELECT *, "Fines" as tipo  FROM itens_fines WHERE dia_id = %s
                UNION ALL
                SELECT *, "STS" as tipo  FROM itens_sts WHERE dia_id = %s
            )as sub;

            """, (id, id, id))
            
            response = cursor.fetchall()
            return response
    finally:
        conn.close