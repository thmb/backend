"""Services module for business logic and data manipulation."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .product_service import ProductService


def get_product_service(db: Annotated[Session, Depends(get_db)]) -> ProductService:
    """Create ProductService instance with database session."""
    return ProductService(db=db)


# Type alias for cleaner route signatures
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
