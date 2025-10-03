from fastapi import FastAPI
from src.routes import pmd_router
from src.middlaware.auth_middlaware import middleware_authentication
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth_router, user_router
#Deinicia a aplicação fast api
app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

#middawere de segurança
app.middleware("http")(middleware_authentication)

# Adicione o middleware antes de definir as rotas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # qualquer domínio
    allow_credentials=True,
    allow_methods=["*"],        # permite GET, POST, PUT, DELETE, OPTIONS...
    allow_headers=["*"],
)

#Altorizações do app
app.include_router(auth_router.router)

#Altorizações do app
app.include_router(user_router.router)

#Rotas do pmd
app.include_router(pmd_router.router)