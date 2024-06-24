from fastapi import APIRouter, Depends
from db import get_session
from models.classes import Smell, Smell_Main, Tags, New_Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union

smell_router = APIRouter(tags=[Tags.smell], prefix="/routers/smell_router")


@smell_router.get("/", response_model=Union[list[Smell_Main], New_Response], tags=[Tags.smell])
def get_smell(db: Session = Depends(get_session)):
    smells = db.query(Smell).all()
    if smells is None:
        return JSONResponse(status_code=404, content={"message": "Степени запаха не найдены"})
    return smells


@smell_router.get("/{id_smell}", response_model=Union[Smell_Main, New_Response], tags=[Tags.smell])
def get_smell(id_smell: int, db: Session = Depends(get_session)):
    smell = db.query(Smell).filter(Smell.id_smell == id_smell).first()
    if smell is None:
        return JSONResponse(status_code=404, content={"message": "Степень запаха не найдена"})
    return smell
