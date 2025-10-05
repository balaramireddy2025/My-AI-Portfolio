from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/demo")
def demo_index(request: Request):
    return templates.TemplateResponse("demos.html", {"request": request})

@router.post("/demo/text-generator")
def text_generator(request: Request, input_text: str = Form(...)):
    # Placeholder AI: reverses input text
    output_text = input_text[::-1]
    return templates.TemplateResponse("demos.html", {"request": request, "input_text": input_text, "output_text": output_text})
