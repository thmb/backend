'''Product service for PostgreSQL database operations.'''
from datetime import datetime
from uuid import UUID, uuid7

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..models.product import Product


class ProductService:
    '''Service for product CRUD operations using PostgreSQL.'''

    def __init__(self, db: Session):
        '''Initialize with database session.'''
        self.db = db

    def create(self, name: str) -> Product:
        '''Create a new product.'''
        product = Product(
            id=uuid7(),
            name=name,
            version=datetime.now(),
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_all(self, name_filter: str | None = None) -> list[Product]:
        '''Get all products with optional name filter.'''
        query = select(Product)
        if name_filter:
            query = query.where(Product.name.ilike(f'%{name_filter}%'))
        return list(self.db.scalars(query).all())

    def get_by_id(self, product_id: UUID) -> Product | None:
        '''Get a product by ID.'''
        return self.db.get(Product, product_id)

    def update(self, product_id: UUID, name: str | None = None) -> Product | None:
        '''Update a product.'''
        product = self.get_by_id(product_id)
        if not product:
            return None

        if name is not None:
            product.name = name
        product.version = datetime.now()

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: UUID) -> bool:
        '''Delete a product.'''
        product = self.get_by_id(product_id)
        if not product:
            return False

        self.db.delete(product)
        self.db.commit()
        return True

    def count(self) -> int:
        '''Get total count of products.'''
        return self.db.scalar(select(func.count()).select_from(Product)) or 0
