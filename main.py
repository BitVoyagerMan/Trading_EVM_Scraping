from fastapi import FastAPI
from backend.api.app.routers import default
from backend.api.app.routers import getMainInfo
from backend.api.app.routers import getInfoByScraping
from backend.api.app.routers import getPolygonInfoByScraping
#from backend.api.core.config import settings
import uvicorn
def include_router(app):
    app.include_router(default.router)
    app.include_router(getMainInfo.router)
    app.include_router(getInfoByScraping.router)
    app.include_router(getPolygonInfoByScraping.router)

app = FastAPI(title = "settings.APP_TITLE", version = 1.0)
include_router(app)

# if __name__ == "__main__":
#      app = start_application()
#      uvicorn.run(app, port = 80)