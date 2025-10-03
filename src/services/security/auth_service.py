#Responsavel pela comunicação com serviços para funcoes relacionadas a auth

# ---------------- Imports Externos ----------------
# ---------------- Imports Externos ----------------

# ---------------- Imports Internas ----------------
from src.db.database import get_connection
# ---------------- Imports Internas ----------------


async def get_refresh_token_in_db_by_id(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT refresh_token FROM users WHERE id = %s
            """, (id))

            response = cursor.fetchone()

            return response

    finally:
        conn.close()

async def insert_refresh_token_in_db(refresh_token, id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE users 
            SET refresh_token = %s
            WHERE id = %s               
            """, (refresh_token, id))
        conn.commit()
    finally:
        conn.close()