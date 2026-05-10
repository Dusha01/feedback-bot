import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.api.routes import rt as rt_forms



app = FastAPI(
    title="Dusha fullstack API",
    description="API для обработки контактных форм с отправкой в Telegram",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


app.include_router(rt_forms)


@app.get("/")
async def root():
    return {"message": "Contact Form API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    logging.info("Starting up Contact Form API...")


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down Contact Form API...")


def main():
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG
    )


if __name__ == "__main__":
    main()