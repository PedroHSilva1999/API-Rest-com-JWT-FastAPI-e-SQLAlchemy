import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.configs import settings
from core.deps import get_session
from models.products import Product
from models.users import User
from schemas.product_schema import ProductSchema
from security.auth import get_current_user


router = APIRouter()

@router.post("/create_product", response_model=ProductSchema)
async def create_product(product: ProductSchema, db: AsyncSession = Depends(get_session) , current_user: User = Depends(get_current_user)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        is_active=product.is_active,
        created_by=current_user.id,
        updated_by=current_user.id
    )
    db.add(new_product)
    await db.commit()
    return new_product
    
@router.get("/get_products", response_model=list[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    products = await db.execute(select(Product))
    return products.scalars().all()

@router.get("/get_product_by_id/{product_id}", response_model=ProductSchema)
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    product = await db.execute(select(Product).filter(Product.id == product_id))
    return product.scalar_one_or_none()

@router.put("/update_product/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product: ProductSchema, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        is_active=product.is_active,
        created_by=current_user.id,
        updated_by=current_user.id,
        updated_at=datetime.datetime.now()
    )

    async with db as session:
        query = select(Product).filter(Product.id == product_id)
        result = await session.execute(query)
        product_db = result.scalar_one_or_none()
        if product_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
        
        product_db.name = new_product.name
        product_db.description = new_product.description
        product_db.price = new_product.price
        product_db.stock = new_product.stock
        product_db.is_active = new_product.is_active
        product_db.updated_by = new_product.updated_by
        product_db.updated_at = new_product.updated_at

        session.add(product_db)
        await session.commit()
        return product_db

@router.delete("/delete_product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    product_db = await db.execute(select(Product).filter(Product.id == product_id))
    product_db = product_db.scalar_one_or_none()
    if product_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    
    await db.delete(product_db)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


