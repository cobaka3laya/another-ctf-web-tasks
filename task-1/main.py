from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {
        "request": request,
        "title": "Магазин глупостей",
        "products": [
            {"name": "Флаг", "price": 0, "image_url": "/static/images/flag.png"},
            {"name": "Глупость 2", "price": 100, "image_url": "/static/images/zazu.jpg"},
            {"name": "Глупость 3", "price": 0, "image_url": "/static/images/zazu.jpg"},
        ],
    }

    return template.TemplateResponse("main.html", context)
