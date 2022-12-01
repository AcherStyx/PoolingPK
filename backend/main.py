from fastapi import FastAPI
from game_env.poolingpk import PoolingPK
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

envs = {
    "0": PoolingPK()
}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/pooling_pk/{env_id}/get_status")
async def pooling_pk_env(env_id):
    return envs[env_id].scan(None)
