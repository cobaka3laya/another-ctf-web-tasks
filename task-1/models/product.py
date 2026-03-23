from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: str
    name: str
    price: float
    image_url: Optional[str]
    url: Optional[str] = None