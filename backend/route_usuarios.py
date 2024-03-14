from fastapi import  APIRouter, FastAPI, Depends, HTTPException, status, Response

from  database import engine,SessionLocal, Base
from schema import UsuarioSchema
from sqlalchemy.orm import Session
from models import User

#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/User")   

def get_db():
    try:
        db = SessionLocal()
        #TODO 
        yield db
    finally:
        db.close()




@router.post("/add")
async def add_usuario(request:UsuarioSchema, db: Session = Depends(get_db)):
    usuario_on_db = User(id=request.id, item=request.item, peso=request.peso, numero_caixas=request.numero_caixas)
    db.add(usuario_on_db)
    db.commit()
    db.refresh(usuario_on_db)
    return usuario_on_db

@router.get("/{usuario_name}", description="Listar o usuario pelo nome")
def get_usuarios(usuario_name,db: Session = Depends(get_db)):
    usuario_on_db= db.query(User).filter(User.item == usuario_name).first()
    return usuario_on_db

@router.get("/usuario/listar")
async def get_tarefas(db: Session = Depends(get_db)):
    usuario= db.query(usuario).all()
    return usuario


@router.delete("/{id}", description="Deletar o usuario pelo id")
def delete_usuario(id: int, db: Session = Depends(get_db)):
    usuario_on_db = db.query(User).filter(User.id == id).first()
    if usuario_on_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sem usuario com este id')
    db.delete(usuario_on_db)
    db.commit()
    return f"Banco with id {id} deletado.", Response(status_code=status.HTTP_200_OK)

# @app.put("/usuario/{id}",response_model=usuarios)
# async def update_usuario(request:usuariosSchema, id: int, db: Session = Depends(get_db)):
#     usuario_on_db = db.query(usuarios).filter(usuarios.id == id).first()
#     print(usuario_on_db)
#     if usuario_on_db is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sem usuario com este id')
#     usuario_on_db = usuarios(id=request.id, item=request.item, peso=request.peso, numero_caixas=request.numero_caixas)
#     db.up
#     db.(usuario_on_db)
#     db.commit()
#     db.refresh(usuario_on_db)
#     return usuario_on_db, Response(status_code=status.HTTP_204_NO_CONTENT)


# router = APIRouter()