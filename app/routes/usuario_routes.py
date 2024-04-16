from fastapi import HTTPException, status, Response, Depends, APIRouter
from db.database import engine
from db.deps import get_db_session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from repository.usuario import UsuariosRepository
from db.models import Usuarios as UsuariosModel
from schemas.usuario import Usuarios, UsuariosRequest, UsuariosResponse
router = APIRouter(prefix='/user')

@router.post("/register", status_code=status.HTTP_201_CREATED)
def create(request: UsuariosRequest, db: Session = Depends(get_db_session)):
    ok= UsuariosRepository.save(db, UsuariosModel(**request.dict()))
    return "ok"

# @router.post("/criar", response_model=UsuariosResponse, status_code=status.HTTP_201_CREATED)
# def create(request: UsuariosRequest, db: Session = Depends(get_db)):
#     produto = UsuariosRepository.save(db, UsuariosModel(**request.dict()))
#     return UsuariosResponse.from_orm(produto)
@router.get("/procurar_por_id/{username}", response_model=UsuariosResponse)
def find_by_name(username: str, db: Session = Depends(get_db_session)):
    usuario = UsuariosRepository.find_by_name(db, username)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    return UsuariosResponse.from_orm(usuario)
from fastapi.security import OAuth2PasswordRequestForm



@router.post('/login')
def user_login(
    login_request_form: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)
):
    uc = UsuariosRepository(db_session=db_session)

    user = Usuarios(
        username=login_request_form.username,
        password=login_request_form.password
    )

    token_data = uc.user_login(user=user, expires_in=60)

    return token_data
# @router.get("/testar")
# def validador():
#     teste = UsuariosRepository.validador()