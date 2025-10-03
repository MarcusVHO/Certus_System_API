# Middawares responsavel por authenticar todas as rotas

# ---------------- Imports Externos ----------------
import os
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
# ---------------- Imports Externos ----------------

IGNORE_PATHS = ["/auth/login", "/auth/refresh_token"]

async def middleware_authentication(request:Request, call_next):
    try:
        secret = os.getenv("SECRET")
        algorithm = os.getenv("ALGORITHM")

        if request.url.path in IGNORE_PATHS:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        header_token = None

        if auth_header and auth_header.startswith("Bearer "):
            header_token = auth_header.split(" ")[1]

            payload  = jwt.decode(header_token, secret, algorithms=algorithm)
            print(payload)

            if payload:
                try:
                    response = await call_next(request)

                except Exception as e:
                    return JSONResponse(content={"error": str(e)}, status_code=500)
                
                return response
            
            

        else:
             return JSONResponse(
                status_code=401,
                content={"detail": "Token ausente"}
            )   
    
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Token expirado"}
        )
    
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Token invalido"}
        )