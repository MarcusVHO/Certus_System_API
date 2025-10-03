# Responsavel por estabelecer conexção com banco de dados mysql

# ---------------- Imports Externos ----------------
import os
from dotenv import load_dotenv
import pymysql
# ---------------- Imports Externos ----------------

#Carrega arquivo de ambiente
load_dotenv()

#Estabelece conexção
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database="CERTUS",
        cursorclass=pymysql.cursors.DictCursor
    )



