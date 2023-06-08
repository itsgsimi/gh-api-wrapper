from fastapi import FastAPI
from github import gh_router

app = FastAPI()

app.include_router(gh_router)