"""Product schemas for request/response validation."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base Product schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Product name")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    
    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""
    
    name: str | None = Field(None, min_length=1, max_length=255, description="Product name")


class ProductResponse(ProductBase):
    """Schema for product response."""
    
    id: UUID = Field(..., description="Product unique identifier")
    version: datetime = Field(..., description="Timestamp of last modification")
    
    class Config:
        from_attributes = True
