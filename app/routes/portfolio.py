from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

projects = [
    {
        "title": "AI Text Generator",
        "description": "Generate text using GPT-based models",
        "image": "/static/images/project1.png",
        "github": "https://github.com/yourprofile/text-generator"
    },
    {
        "title": "Image Classifier",
        "description": "Classify images with CNN",
        "image": "/static/images/project2.png",
        "github": "https://github.com/yourprofile/image-classifier"
    }
]

@router.get("/portfolio")
def portfolio(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request, "projects": projects})
