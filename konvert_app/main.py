from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from konvert_app.core.database import Base, engine
from konvert_app.routers import auth, convert, pages

app = FastAPI(title="Konvert")

# Templates
templates = Jinja2Templates(directory="konvert_app/templates")

# Static files
app.mount("/static", StaticFiles(directory="konvert_app/static"), name="static")

# Routers (NO PREFIX HERE)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(convert.router, prefix="/convert", tags=["Convert"])
app.include_router(pages.router)


# DB init
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
