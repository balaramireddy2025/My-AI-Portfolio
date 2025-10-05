from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from markdown2 import markdown
import os

app = FastAPI(title="Taanu AI Portfolio")
templates = Jinja2Templates(directory="app/templates")

# Test email config (prints to console)
conf = ConnectionConfig(
    MAIL_USERNAME="test@example.com",
    MAIL_PASSWORD="test",
    MAIL_FROM="test@example.com",
    MAIL_PORT=25,
    MAIL_SERVER="localhost",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False
)

# Sample portfolio projects
projects = [
    {"title": "AI Project 1", "description": "AI model for image classification", "image": "/static/images/project1.png", "link": "#"},
    {"title": "AI Project 2", "description": "NLP chatbot using Transformers", "image": "/static/images/project2.png", "link": "#"},
    {"title": "AI Project 3", "description": "Text-to-image generation with AI", "image": "/static/images/project1.png", "link": "#"}
]

# Load blog posts
def load_blog_posts():
    blog_dir = "content/blog"
    posts = []
    if os.path.exists(blog_dir):
        for filename in os.listdir(blog_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(blog_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    html_content = markdown(f.read())
                    posts.append({"title": filename[:-3].replace("_"," ").title(), "content": html_content})
    return posts

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "projects": projects,
        "blog_posts": load_blog_posts()
    })

@app.post("/contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    msg = MessageSchema(
        subject=f"Portfolio Contact: {name}",
        recipients=["test@example.com"],
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(msg)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "projects": projects,
        "blog_posts": load_blog_posts(),
        "success": "Message sent successfully!"
    })