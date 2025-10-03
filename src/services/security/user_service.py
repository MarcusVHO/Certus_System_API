#Responsavel pela comunicação com serviços para funcoes relacionadas a usuário

# ---------------- Imports Externos ----------------
# ---------------- Imports Externos ----------------

# ---------------- Imports Internas ----------------
from src.db.database import get_connection
# ---------------- Imports Internas ----------------


#verifica se usário existe no banco de dados atraves de seu id ou oneid
async def find_user_in_db(oneid=None, id=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT id, name, oneid, password, role FROM users WHERE oneid = %s or id = %s""",
            (oneid, id))

            result = cursor.fetchone()
            return result
    finally:
        conn.close()


async def register_new_user_in_db(username, oneid, password, role):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            INSERT INTO users (name, oneid, password, role) VALUES (%s, %s, %s, %s)""",
            (username, oneid, password, role))
            conn.commit()
            print(f"Usuário: {oneid}, inserido com sucesso no banco de dados")

    finally:
        conn.close()