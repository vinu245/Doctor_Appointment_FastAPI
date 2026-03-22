from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from main import app as api_app

app = FastAPI(title="MediCare App Shell")

# Keep the original API untouched and expose it under /api.
app.mount("/api", api_app)
app.mount("/icons", StaticFiles(directory="web/icons"), name="icons")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse("web/index.html")


@app.get("/style.css", include_in_schema=False)
def style():
    return FileResponse("web/style.css", media_type="text/css")


@app.get("/app.js", include_in_schema=False)
def script():
    return FileResponse("web/app.js", media_type="application/javascript")


@app.get("/manifest.json", include_in_schema=False)
def manifest():
    return FileResponse("web/manifest.json", media_type="application/manifest+json")


@app.get("/service-worker.js", include_in_schema=False)
def service_worker():
    return FileResponse("web/service-worker.js", media_type="application/javascript")
