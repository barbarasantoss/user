from decouple import config
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi import status
from schemas.usuario import Usuarios, TokenData
from db.models import Usuarios as UsuariosModel
crypt_context = CryptContext(schemes=['sha256_crypt'])
SECRET_KEY = "  "  
ALGORITHM = "HS256"
class UsuariosRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    @staticmethod
    def save(db: Session, user: Usuarios):
        user_on_db = UsuariosModel(
            username=user.username,
            password=crypt_context.hash(user.password)
        )
        db.add(user_on_db)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')
    
    def user_login(self, user: Usuarios, expires_in: int = 30):
        user_on_db = self._get_user(username=user.username)
    
        if user_on_db is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Username or password does not exist')

        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Username or password does not exist')
        
        expires_at = datetime.utcnow() + timedelta(expires_in)

        data = {
            'sub': user_on_db.username,
            'exp': expires_at
        }

        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        token_data = TokenData(access_token=access_token, expires_at=expires_at)
        return token_data
    
    def verify_token(self, token: str):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        
        user_on_db = self._get_user(username=data['sub'])

        if user_on_db is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    def find_by_name(self, username: str):
        user_on_db = self.query(UsuariosModel).filter_by(username=username).first()
        return user_on_db
    
    def _get_user(self, username: str):
        user_on_db = self.db_session.query(UsuariosModel).filter_by(username=username).first()
        return user_on_db
