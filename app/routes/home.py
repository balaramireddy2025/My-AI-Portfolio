from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request: Request):
    profile = {
        "name": "Your Name",
        "bio": "AI enthusiast | Python developer | Researcher",
        "image": "/static/images/profile.jpg",
        "social": {
            "LinkedIn": "https://linkedin.com/in/yourprofile",
            "GitHub": "https://github.com/yourprofile"
        }
    }
    return templates.TemplateResponse("home.html", {"request": request, "profile": profile})
