from os import getenv

from aws_lambda_powertools import Logger, Tracer
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from mangum import Mangum

service_name = getenv("SERVICE_NAME")

logger = Logger(service=service_name)
tracer = Tracer(service=service_name)

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)


@app.middleware("http")
async def add_tracing_and_logging(request: Request, call_next):
    tracer.put_annotation("path", request.url.path)
    response = await call_next(request)
    logger.info(
        "Request processed",
        extra={
            "path": request.url.path,
            "method": request.method,
        },
    )
    return response


def convert_to_handler(app: FastAPI) -> Mangum:
    return Mangum(app)
