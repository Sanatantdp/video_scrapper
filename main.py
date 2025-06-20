from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI
from router import app_router
import os


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    """
    STATIC_ROOT = os.getcwd()

    app = FastAPI(title="360 Diamond", version="1.0.0")
    app.include_router(app_router)

    app.mount(
        "/static", StaticFiles(directory=f"{STATIC_ROOT}/static", html=True), name="static")
    app.mount("/imagedata",
              StaticFiles(directory=f"{STATIC_ROOT}/imagedata", html=True), name="imagedata")
    app.mount("/css", StaticFiles(directory=f"{STATIC_ROOT}/css"), name="css")
    app.mount("/js", StaticFiles(directory=f"{STATIC_ROOT}/js"), name="js")
    app.mount(
        "/images", StaticFiles(directory=f"{STATIC_ROOT}/images"), name="images")
    app.mount(
        "/imaged", StaticFiles(directory=f"{STATIC_ROOT}/imaged"), name="imaged")
    return app


app = create_app()

if __name__ == "__main__":
    # Run the application with specified host and port
    uvicorn.run("main:app", host="192.168.29.71", port=2500, reload=True)
