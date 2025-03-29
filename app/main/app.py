from fastapi import FastAPI,HTTPException
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from app.api.v1.endpoints.routers import routers
from app.database.db import create_tables
from contextlib import asynccontextmanager
#add CORS
from fastapi.middleware.cors import CORSMiddleware




origins = [
    "http://localhost:3000",
]

@asynccontextmanager
async def init_db(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(title="Audio Service API",lifespan=init_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)


app.include_router(routers)







#if __name__ == "__main__":
#    uvicorn.run(f"{__name__}:app",host="127.0.0.1", port=8080, reload=True)

