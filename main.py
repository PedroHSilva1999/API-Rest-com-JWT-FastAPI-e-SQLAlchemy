from fastapi import FastAPI
from core.configs import settings
from api.api import api_router

app = FastAPI(title="API de Usuários")

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
