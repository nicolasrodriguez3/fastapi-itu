import uvicorn

from app.configs import settings

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="127.0.0.1", port=settings.PORT, reload=settings.DEV)