from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from services import user as services_user
from dto import user as dto_user

router = APIRouter()

@router.post('/', tags=["user"])
async def create(data: dto_user.User = None, db: Session = Depends(get_db)):
    return  services_user.create_user(data, db)

@router.get('/{id}', tags=["user"])
async def get(id: str = None, db: Session=Depends(get_db)):
    return  services_user.get_user(id, db)

@router.put('/{id}', tags=["user"])
async def update(id: int = None, data: dto_user.User = None, db: Session = Depends(get_db)):
    return  services_user.update(data, db, id)

@router.delete('/{id}', tags=["user"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return  services_user.remove(db, id)