from fastapi import APIRouter, Depends, HTTPException, Body
from db import get_session
from models.classes import Printing_technology, Printing_technology_Main, Tags, New_Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union, Annotated
from starlette import status

technology_router = APIRouter(tags=[Tags.technology], prefix="/routers/technology_router")


@technology_router.get("/", response_model=Union[list[Printing_technology_Main], New_Response],
                       tags=[Tags.technology])
def get_printing_technologies(db: Session = Depends(get_session)):
    printing_technologies = db.query(Printing_technology).all()
    if printing_technologies is None:
        return JSONResponse(status_code=404, content={"message": "Технологии печати не найдены"})
    return printing_technologies


@technology_router.get("/{id_technology}",
                       response_model=Union[Printing_technology_Main, New_Response], tags=[Tags.technology])
def get_printing_technology(id_technology: int, db: Session = Depends(get_session)):
    printing_technology = db.query(Printing_technology).filter(
        Printing_technology.id_technology == id_technology).first()
    if printing_technology is None:
        return JSONResponse(status_code=404, content={"message": "Технология печати не найдена"})
    return printing_technology


@technology_router.post("/", response_model=Union[Printing_technology_Main, New_Response],
                        tags=[Tags.technology], status_code=status.HTTP_201_CREATED)
def create_printing_technology(
        item: Annotated[Printing_technology_Main, Body(embed=True, description="Новая технология печати")],
        db: Session = Depends(get_session)):
    try:
        printing_technology = Printing_technology(name_printing_technology=item.name_printing_technology)
        if printing_technology is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        db.add(printing_technology)
        db.commit()
        db.refresh(printing_technology)
        return printing_technology
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {printing_technology}")


@technology_router.put("/", response_model=Union[Printing_technology_Main, New_Response],
                       tags=[Tags.technology])
def edit_printing_technology(
        item: Annotated[Printing_technology_Main,
                        Body(embed=True, description="Изменение данных технологии печати по id")],
        db: Session = Depends(get_session)):
    printing_technology = db.query(Printing_technology).filter(
        Printing_technology.id_technology == item.id_technology).first()
    if printing_technology is None:
        return JSONResponse(status_code=404, content={"message": "Технология печати не найдена"})
    printing_technology.name_printing_technology = item.name_printing_technology
    try:
        db.commit()
        db.refresh(printing_technology)
    except HTTPException:
        return JSONResponse(status_code=404,
                            content={"message": "Произошла ошибка при изменении объекта {printing_technology}"})
    return printing_technology


@technology_router.delete("/{id_technology}", response_class=JSONResponse, tags=[Tags.technology])
def delete_printing_technology(id_technology: int, db: Session = Depends(get_session)):
    printing_technology = db.query(Printing_technology).filter(
        Printing_technology.id_technology == id_technology).first()
    if printing_technology is None:
        return JSONResponse(status_code=404, content={"message": "Технология печати не найдена"})
    try:
        db.delete(printing_technology)
        db.commit()
    except HTTPException:
        JSONResponse(content={'message': f'Произошла ошибка при удалении объекта {printing_technology}'})
    return JSONResponse(content={'message': f'Технология печати удалена {id_technology}'})

