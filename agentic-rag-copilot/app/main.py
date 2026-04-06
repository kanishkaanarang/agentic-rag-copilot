from fastapi import FastAPI
from pydantic import BaseModel
from agent.planner import plan
from agent.executor import execute

from rag.ingest import ingest_document
import os
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading knowledge base...")

    data_folder = "data"

    for file in os.listdir(data_folder):
        if file.endswith(".pdf"):
            ingest_document(os.path.join(data_folder, file))

    print("Knowledge base ready")

    yield  # app runs here

    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask(req: QueryRequest):
    try:
        answer = execute(req.query, [req.query])
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}