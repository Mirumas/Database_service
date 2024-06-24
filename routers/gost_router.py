from fastapi import APIRouter, Depends, HTTPException, Body
from db import get_session
from models.classes import Gost, Gost_Main, Tags, New_Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union, Annotated
from starlette import status

gost_router = APIRouter(tags=[Tags.gost], prefix="/routers/gost_router")


@gost_router.get("/", response_model=Union[list[Gost_Main], New_Response], tags=[Tags.gost])
def get_gosts(db: Session = Depends(get_session)):
    gosts = db.query(Gost).all()
    if gosts is None:
        return JSONResponse(status_code=404, content={"message": "ГОСТы не найдены"})
    return gosts


@gost_router.get("/{id_gost}", response_model=Union[Gost_Main, New_Response], tags=[Tags.gost])
def get_gost(id_gost: int, db: Session = Depends(get_session)):
    gost = db.query(Gost).filter(Gost.id_gost == id_gost).first()
    if gost is None:
        return JSONResponse(status_code=404, content={"message": "ГОСТ не найден"})
    return gost


@gost_router.post("/", response_model=Union[Gost_Main, New_Response],
                  tags=[Tags.gost], status_code=status.HTTP_201_CREATED)
def create_gost(item: Annotated[Gost_Main, Body(embed=True, description="Новый ГОСТ")],
                db: Session = Depends(get_session)):
    try:
        gost = Gost(name_gost=item.name_gost)
        if gost is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        db.add(gost)
        db.commit()
        db.refresh(gost)
        return gost
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {gost}")


@gost_router.put("/", response_model=Union[Gost_Main, New_Response], tags=[Tags.gost])
def edit_gost(item: Annotated[Gost_Main, Body(embed=True, description="Изменение данных ГОСТа по id")],
              db: Session = Depends(get_session)):
    gost = db.query(Gost).filter(Gost.id_gost == item.id_gost).first()
    if gost is None:
        return JSONResponse(status_code=404, content={"message": "ГОСТ не найден"})
    gost.name_gost = item.name_gost
    try:
        db.commit()
        db.refresh(gost)
    except HTTPException:
        return JSONResponse(status_code=404,
                            content={"message": "Произошла ошибка при изменении объекта {gost}"})
    return gost


@gost_router.delete("/{id_gost}", response_class=JSONResponse, tags=[Tags.gost])
def delete_gost(id_gost: int, db: Session = Depends(get_session)):
    gost = db.query(Gost).filter(Gost.id_gost == id_gost).first()
    if gost is None:
        return JSONResponse(status_code=404, content={"message": "ГОСТ не найден"})
    try:
        db.delete(gost)
        db.commit()
    except HTTPException:
        JSONResponse(content={'message': f'Произошла ошибка при удалении объекта {gost}'})
    return JSONResponse(content={'message': f'ГОСТ удален {id_gost}'})
