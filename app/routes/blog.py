
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
import markdown2
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
BLOG_DIR = "content/blog"

@router.get("/blog")
def blog_list(request: Request):
    posts = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(BLOG_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
            posts.append({"title": first_line, "slug": filename.replace(".md", "")})
    return templates.TemplateResponse("blog_list.html", {"request": request, "posts": posts})

@router.get("/blog/{slug}")
def blog_post(request: Request, slug: str):
    filepath = os.path.join(BLOG_DIR, slug + ".md")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Post not found")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    html_content = markdown2.markdown(content)
    return templates.TemplateResponse("blog_post.html", {"request": request, "content": html_content, "title": slug})