import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import Database
from utils import get_template, get_db

product_router = APIRouter()

@product_router.get("/products/{product_id}", response_class=HTMLResponse)
def get_product_page(
    request: Request,
    product_id: int,
    template: Annotated[Jinja2Templates, Depends(get_template)],
    db: Annotated[Database, Depends(get_db)]
):
    """A get route for getting a product by its id"""
    try:
        current_product = db.get_product_by_id(id)
        
        context = {
            "request": request,
            "title": current_product.name,
            "product": current_product
        }

        path = 'product.html'
        if current_product.name == 'Флаг':
            path = 'flag_product.html'

        return template.TemplateResponse(path, context=context)
    
    except Exception as e:
        err_msg = f'Error during getting product page: {e}'
        logging.error(err_msg)
        raise HTTPException(status_code=400, detail=err_msg)