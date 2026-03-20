import logging
from typing import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

import utils


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(
    request: Request, 
    template: Annotated[Jinja2Templates, Depends(utils.get_template)],
    logger: Annotated[logging.Logger, Depends(utils.get_logger)],
) -> HTMLResponse:
    """Root route."""
    logger.info('test')

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
