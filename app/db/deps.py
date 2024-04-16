from decouple import config
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.database import Session
from repository.usuario import UsuariosRepository

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

def auth(
    db_session: Session = Depends(get_db_session),
    token = Depends(oauth_scheme)
):

    uc = UsuariosRepository(db_session=db_session)
    uc.verify_token(token=token)
