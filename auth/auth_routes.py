from fastapi import APIRouter, Depends, HTTPException
from models.models import User
from dependencies import get_session_db, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas.schemas import UserSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

def get_token(user_id, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    date_expires = datetime.now(timezone.utc) + duration_token
    dic_info = {'sub': str(user_id), 'exp': int(date_expires.timestamp())}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def authorize_user(email, password, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    else:
        return user



@auth_router.get('/')
async def auth():
    return { 'message': 'Authorization' }

@auth_router.post('/create_account')
async def create_account(user_schema: UserSchema, session=Depends(get_session_db)):
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=422, detail=f'Email {user_schema.email} already in use')
    else:
        password_encrypted = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, password_encrypted, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return { 'status': 'OK', 'message': f'User {user_schema.email} created successfully' }
    

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session=Depends(get_session_db)):
    user = authorize_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail='Invalid credentials')
    else:
        access_token = get_token(user.id)
        refresh_token = get_token(user.id, timedelta(days=7))
        return {
            'access_token': access_token, 
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
            }
    

@auth_router.get('/refresh')
async def refresh_token_user(user: User = Depends(verify_token)):
    access_token = get_token(user.id)
    return {
            'access_token': access_token, 
            'token_type': 'Bearer'
            }