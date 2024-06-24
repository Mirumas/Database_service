from fastapi import APIRouter, Depends, HTTPException, Body
from db import get_session
from models.classes import Manufacturer, Manufacturer_Main, Tags, New_Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union, Annotated
from starlette import status

manufacturer_router = APIRouter(tags=[Tags.manufacturer], prefix="/routers/manufacturer_router")


@manufacturer_router.get("/", response_model=Union[list[Manufacturer_Main], New_Response],
                         tags=[Tags.manufacturer])
def get_manufacturers(db: Session = Depends(get_session)):
    manufacturers = db.query(Manufacturer).all()
    if manufacturers is None:
        return JSONResponse(status_code=404, content={"message": "Производители не найдены"})
    return manufacturers


@manufacturer_router.get("/{id_manufacturer}",
                         response_model=Union[Manufacturer_Main, New_Response], tags=[Tags.manufacturer])
def get_manufacturer(id_manufacturer: int, db: Session = Depends(get_session)):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id_manufacturer == id_manufacturer).first()
    if manufacturer is None:
        return JSONResponse(status_code=404, content={"message": "Производитель не найден"})
    return manufacturer


@manufacturer_router.post("/", response_model=Union[Manufacturer_Main, New_Response],
                          tags=[Tags.manufacturer], status_code=status.HTTP_201_CREATED)
def create_manufacturer(item: Annotated[Manufacturer_Main, Body(embed=True, description="Новый производитель")],
                        db: Session = Depends(get_session)):
    try:
        manufacturer = Manufacturer(name_manufacturer=item.name_manufacturer, country=item.country)
        if manufacturer is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        db.add(manufacturer)
        db.commit()
        db.refresh(manufacturer)
        return manufacturer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {manufacturer}")


@manufacturer_router.put("/", response_model=Union[Manufacturer_Main, New_Response], tags=[Tags.manufacturer])
def edit_manufacturer(
        item: Annotated[Manufacturer_Main, Body(embed=True, description="Изменение данных производителя по id")],
        db: Session = Depends(get_session)):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id_manufacturer == item.id_manufacturer).first()
    if manufacturer is None:
        return JSONResponse(status_code=404, content={"message": "Материал не найден"})
    manufacturer.name_manufacturer = item.name_manufacturer
    manufacturer.country = item.country
    try:
        db.commit()
        db.refresh(manufacturer)
    except HTTPException:
        return JSONResponse(status_code=404,
                            content={"message": "Произошла ошибка при изменении объекта {manufacturer}"})
    return manufacturer


@manufacturer_router.delete("/{id_manufacturer}", response_class=JSONResponse, tags=[Tags.manufacturer])
def delete_manufacturer(id_manufacturer: int, db: Session = Depends(get_session)):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id_manufacturer == id_manufacturer).first()
    if manufacturer is None:
        return JSONResponse(status_code=404, content={"message": "Производитель не найден"})
    try:
        db.delete(manufacturer)
        db.commit()
    except HTTPException:
        JSONResponse(content={'message': f'Произошла ошибка при удалении объекта {manufacturer}'})
    return JSONResponse(content={'message': f'Производитель удалён {id_manufacturer}'})


@manufacturer_router.patch("/{id_manufacturer}",
                           response_model=Union[Manufacturer_Main, New_Response], tags=[Tags.manufacturer])
def edit_manufacturer(
        item: Annotated[Manufacturer_Main, Body(embed=True, description="Изменение данных производителя по id")],
        id_manufacturer: int, db: Session = Depends(get_session)):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id_manufacturer == id_manufacturer).first()
    if manufacturer is None:
        return JSONResponse(status_code=404, content={"message": "Материал не найден"})

    if item.name_manufacturer is not None:
        manufacturer.name_manufacturer = item.name_manufacturer
    if item.country is not None:
        manufacturer.country = item.country

    try:
        db.commit()
        db.refresh(manufacturer)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"message": f"Произошла ошибка при обновлении объекта: {str(e)}"})
    return manufacturer
