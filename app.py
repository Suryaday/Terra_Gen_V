from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import (
    GenerateRequest,
    GenerateResponse
)

from generator import generate

import time

app = FastAPI(title="Terraform AI Architect", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "running"
    }

@app.post(
    "/generate",
    response_model=GenerateResponse
)

def generate_terraform(request: GenerateRequest):

    start = time.perf_counter()

    result = generate(request.query)

    elapsed = (time.perf_counter() - start)

    architecture = [
        node.entity
        for node
        in result.plan.ordered_nodes
    ]

    terraform = result.files.get("main.tf", "")

    return GenerateResponse(
        query=request.query,
        architecture=architecture,
        terraform=terraform,
        warnings=result.warnings,
        generation_time_seconds=round(
            elapsed,
            2
        )
    )