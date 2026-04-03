from fastapi import FastAPI

from api.routes.auth import router as auth_router
from api.routes.quiz import router as quiz_router


app = FastAPI(title="NeuroCognitive Engine API")
app.include_router(auth_router)
app.include_router(quiz_router)
