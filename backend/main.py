from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import schedules, export

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Campus Smart Scheduler API",
    description="API for managing, analyzing, and exporting college class schedules.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schedules.router)
app.include_router(export.router)


@app.get("/health")
def health():
    return {"status": "ok"}
