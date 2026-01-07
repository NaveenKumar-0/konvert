from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="konvert_app/templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/verify-email")
def verify_email_page(request: Request, token: str):
    return templates.TemplateResponse(
        "verify.html",
        {
            "request": request,
            "token": token
        }
    )

@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/image")
def image_page(request: Request):
    return templates.TemplateResponse("image.html", {"request": request})


@router.get("/video")
def video_page(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})