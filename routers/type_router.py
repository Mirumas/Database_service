from fastapi import APIRouter, Depends, HTTPException, Body
from db import get_session
from models.classes import Type_of_material, Type_of_material_Main, Tags, New_Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union, Annotated
from starlette import status

type_router = APIRouter(tags=[Tags.type], prefix="/routers/type_router")


@type_router.get("/", response_model=Union[list[Type_of_material_Main], New_Response], tags=[Tags.type])
def get_types(db: Session = Depends(get_session)):
    types = db.query(Type_of_material).all()
    if types is None:
        return JSONResponse(status_code=404, content={"message": "Виды материалов не найдены"})
    return types


@type_router.get("/{id_type}", response_model=Union[Type_of_material_Main, New_Response], tags=[Tags.type])
def get_type(id_type: int, db: Session = Depends(get_session)):
    type = db.query(Type_of_material).filter(Type_of_material.id_type == id_type).first()
    if type is None:
        return JSONResponse(status_code=404, content={"message": "Вид материала не найден"})
    return type


@type_router.post("/", response_model=Union[Type_of_material_Main, New_Response],
                  tags=[Tags.type], status_code=status.HTTP_201_CREATED)
def create_type(item: Annotated[Type_of_material_Main, Body(embed=True, description="Новый вид материала")],
                db: Session = Depends(get_session)):
    try:
        type = Type_of_material(name_type=item.name_type)
        if type is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        db.add(type)
        db.commit()
        db.refresh(type)
        return type
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {type}")


@type_router.put("/", response_model=Union[Type_of_material_Main, New_Response], tags=[Tags.type])
def edit_type(item: Annotated[Type_of_material_Main,
                              Body(embed=True, description="Изменение данных вида материала по id")],
              db: Session = Depends(get_session)):
    type = db.query(Type_of_material).filter(Type_of_material.id_type == item.id_type).first()
    if type is None:
        return JSONResponse(status_code=404, content={"message": "Вид материала не найден"})
    type.name_type = item.name_type
    try:
        db.commit()
        db.refresh(type)
    except HTTPException:
        return JSONResponse(status_code=404,
                            content={"message": "Произошла ошибка при изменении объекта {type}"})
    return type


@type_router.delete("/{id_type}", response_class=JSONResponse, tags=[Tags.type])
def delete_type(id_type: int, db: Session = Depends(get_session)):
    type = db.query(Type_of_material).filter(Type_of_material.id_type == id_type).first()
    if type is None:
        return JSONResponse(status_code=404, content={"message": "Вид материала не найден"})
    try:
        db.delete(type)
        db.commit()
    except HTTPException:
        JSONResponse(content={'message': f'Произошла ошибка при удалении объекта {type}'})
    return JSONResponse(content={'message': f'Вид материала удален {id_type}'})
