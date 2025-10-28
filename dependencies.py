
from fastapi import Depends, HTTPException
from models.models import db, User
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

async def get_session_db():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verify_token(token: str = Depends(oauth2_schema), session=Depends(get_session_db)):
    try:
        dic_info_user = jwt.decode(token, SECRET_KEY, ALGORITHM)
        print(dic_info_user)
        user_id = int(dic_info_user['sub'])
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied, verify expiration token")

    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Access denied")
    
    return user