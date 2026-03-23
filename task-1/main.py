import logging
from typing import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from db import DatabaseSession
from models.product import Product
from routes.products import product_router
import utils


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(product_router)

@app.get("/", response_class=HTMLResponse)
async def root(
    request: Request, 
    template: Annotated[Jinja2Templates, Depends(utils.get_template)],
    logger: Annotated[logging.Logger, Depends(utils.get_logger)],
    db: Annotated[DatabaseSession, Depends(utils.get_db)],
) -> HTMLResponse:
    """Root route."""
    db.add_products([
        Product(0, "Флаг", 50, "/static/images/flag.png")
    ])

    prods = db.get_products(0, 5)

    context = {
        "request": request,
        "title": "Магазин глупостей",
        "products": prods,
    }

    return template.TemplateResponse("main.html", context)
