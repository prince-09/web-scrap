from pydantic import BaseModel
from typing import Optional
from pathlib import Path

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: Optional[Path] = None  # path_to_image can be None
    
    class Config:
        orm_mode = True

    def dict(self):
        return {
            "product_title": self.product_title,
            "product_price": self.product_price,
            "path_to_image": str(self.path_to_image) if self.path_to_image else None
        }


class ScraperSettings(BaseModel):
    pages_to_scrape: Optional[int] = 5
    proxy: Optional[str] = None
