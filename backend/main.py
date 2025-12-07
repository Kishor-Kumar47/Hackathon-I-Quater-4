# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from .app.api.auth import router as auth_router
# from .app.services.qdrant_service import get_qdrant_collections

# app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "http://127.0.0.1",
#     "http://127.0.0.1:3000",
#     "*"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# @app.get("/")
# async def root():
#     return {"message": "Physical AI Book Backend"}

# @app.get("/api/qdrant/collections")
# async def get_collections_endpoint():
#     collections = get_qdrant_collections()
#     return {"collections": collections.collections}

from backend.app.api.auth import router as auth_router
from backend.app.services.qdrant_service import get_qdrant_collections

from fastapi import FastAPI


app = FastAPI()

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Physical AI Book Backend"}

@app.get("/api/qdrant/collections")
async def get_collections_endpoint():
    collections = get_qdrant_collections()
    return {"collections": collections.collections}
