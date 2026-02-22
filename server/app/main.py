from fastapi import FastAPI
from .core import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}", "status": "online"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
