"""Product router with CRUD endpoints."""
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..services import ProductServiceDep


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
async def create_product(
    service: ProductServiceDep,
    product: ProductCreate,
) -> ProductResponse:
    """Create a new product."""
    created = service.create(name=product.name)
    return ProductResponse(
        id=created.id,
        name=created.name,
        version=created.version,
    )


@router.get(
    "/",
    response_model=list[ProductResponse],
    summary="List all products",
)
async def list_products(
    service: ProductServiceDep,
    name: str | None = Query(None, description="Filter products by name (partial match)"),
) -> list[ProductResponse]:
    """Get all products with optional name filter."""
    products = service.get_all(name_filter=name)
    return [
        ProductResponse(id=p.id, name=p.name, version=p.version)
        for p in products
    ]


@router.get(
    "/stats/count",
    response_model=dict,
    summary="Get product count",
)
async def get_product_count(service: ProductServiceDep) -> dict:
    """Get total count of products."""
    count = service.count()
    return {"count": count}


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get a product by ID",
)
async def get_product(
    service: ProductServiceDep,
    product_id: UUID,
) -> ProductResponse:
    """Get a specific product by ID."""
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return ProductResponse(
        id=product.id,
        name=product.name,
        version=product.version,
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a product",
)
async def update_product(
    service: ProductServiceDep,
    product_id: UUID,
    product: ProductUpdate,
) -> ProductResponse:
    """Update an existing product."""
    updated = service.update(
        product_id=product_id,
        name=product.name,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return ProductResponse(
        id=updated.id,
        name=updated.name,
        version=updated.version,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
)
async def delete_product(
    service: ProductServiceDep,
    product_id: UUID,
) -> None:
    """Delete a product by ID."""
    deleted = service.delete(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
