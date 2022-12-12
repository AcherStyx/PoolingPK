from fastapi import FastAPI, Request
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

# token: env instance
envs = {
    "0": PoolingPK()
}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/pooling_pk/{env_id}/get_status")
async def pooling_pk_env_get_status(env_id):
    return envs[env_id].scan(None)


@app.post("/pooling_pk/{env_id}/control")
async def pooling_pk_env_control(env_id, control_info: Request):
    control_info = await control_info.json()
    return envs[env_id].update(control_info)


@app.get("/pooling_pk/{env_id}/restart")
async def pooling_pk_env_restart(env_id):
    envs[env_id] = PoolingPK()
    return "success"
