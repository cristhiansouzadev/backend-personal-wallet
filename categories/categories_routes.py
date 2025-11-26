from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session_db, verify_token
from models.models import Category, User
from schemas.schemas import CategorySchema
from typing import List

category_router = APIRouter(prefix='/categories', tags=['Categories']) 


@category_router.get('/')
async def get_categories():
    return { 'message': 'Categories List' }


@category_router.post('/category')
async def create_category(category_schema: CategorySchema, session=Depends(get_session_db), user: User = Depends(verify_token)):
    new_category = Category(name= category_schema.name)
    session.add(new_category)
    session.commit()
    return { 'message': f'Category created successfully' }


@category_router.get('/list')
async def categories_list(session=Depends(get_session_db), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail='Access denied for this action')
    else:
        categories = session.query(Category).all()

    return { 
        'categories': categories 
    }

