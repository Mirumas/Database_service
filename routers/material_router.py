from fastapi import APIRouter, Depends, HTTPException, Body, Request, Form
from db import get_session
from models.classes import Material, Material_Main, Tags, New_Response, Gost, Smell, Material_parameters, Parameter, Material_with_parameters_Main, Printing_technology, Parameter_Main, Manufacturer
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import Union, Annotated
from starlette import status
from db import templates

material_router = APIRouter(tags=[Tags.material], prefix="/routers/material_router")


@material_router.post("/name")
def get_materials_by_name(request: Request, name_material: str = Form(...), db: Session = Depends(get_session)):
    materials_by_name = (
        db.query(Material.id_material, Material.name_material, Material.price, Gost.name_gost, Smell.degree_smell,
                 Manufacturer.name_manufacturer, Manufacturer.country, Printing_technology.name_technology).select_from(Material)
                .filter(Material.name_material.ilike(f'%{name_material}%'))
                .join(Gost).join(Smell).join(Manufacturer).join(Printing_technology))
    if not materials_by_name.first():
        return JSONResponse(status_code=404, content={"message": "Материал не найден"})
    return templates.TemplateResponse("materials.html", {"request": request, "materials": materials_by_name})


@material_router.get("/", response_model=Union[list[Material_Main], New_Response], tags=[Tags.material], response_class=HTMLResponse)
def get_materials(request: Request, db: Session = Depends(get_session)):
    materials = (db.query(Material.id_material, Material.name_material, Material.price, Gost.name_gost, Smell.degree_smell, Manufacturer.name_manufacturer, Manufacturer.country, Printing_technology.name_technology).
                select_from(Material).join(Gost).join(Smell).join(Manufacturer).join(Printing_technology).all())
    if materials is None:
        return JSONResponse(status_code=404, content={"message": "Материалы не найдены"})
    return templates.TemplateResponse("materials.html", {"request": request, "materials": materials})


@material_router.get("/{id_material}", response_model=Union[Material_with_parameters_Main, New_Response], tags=[Tags.material])
def get_material_by_id(id_material: int, db: Session = Depends(get_session)):
    material = (db.query(Material.id_material, Material.name_material, Material.price, Gost.name_gost, Smell.degree_smell, Manufacturer.name_manufacturer, Manufacturer.country, Material_parameters.value_parameter, Parameter.name_parameter, Printing_technology.name_technology)
                .select_from(Material).filter(Material.id_material == id_material)
                .join(Gost).join(Smell).join(Manufacturer).join(Material_parameters).join(Parameter))
    if material is None:
        return JSONResponse(status_code=404, content={"message": "Материал не найден"})
    return material


@material_router.post("/", response_model=Union[Material_Main, New_Response],
                      tags=[Tags.material], status_code=status.HTTP_201_CREATED)
def create_material(item: Annotated[Material_Main, Body(embed=True, description="Новый материал")],
                    db: Session = Depends(get_session)):
    try:
        material = Material(name_material=item.name_material, price=item.price)
        material.id_type = item.id_type
        material.id_smell = item.id_smell
        material.id_manufacturer = item.id_manufacturer
        if material is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        db.add(material)
        db.commit()
        db.refresh(material)
        return material
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {material}")


@material_router.put("/", response_model=Union[Material_Main, New_Response], tags=[Tags.material])
def edit_material(item: Annotated[Material_Main, Body(embed=True, description="Изменение данных материала по id")],
                  db: Session = Depends(get_session)):
    material = db.query(Material).filter(Material.id_material == item.id_material).first()
    if material is None:
        return JSONResponse(status_code=404, content={"message": "Материал не найден"})
    material.name_material = item.name_material
    material.price = item.price
    material.id_type = item.id_type
    material.id_smell = item.id_smell
    material.id_manufacturer = item.id_manufacturer
    try:
        db.commit()
        db.refresh(material)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": "Произошла ошибка при изменении объекта {material}"})
    return material


@material_router.delete("/{id_material}", response_class=JSONResponse, tags=[Tags.material])
def delete_material(id_material: int, db: Session = Depends(get_session)):
    material = db.query(Material).filter(Material.id_material == id_material).first()
    if material is None:
        return JSONResponse(status_code=404, content={"message": "Материал не найден"})
    try:
        db.delete(material)
        db.commit()
    except HTTPException:
        JSONResponse(content={'message': f'Произошла ошибка при удалении объекта {material}'})
    return JSONResponse(content={'message': f'Материал удалён {id_material}'})


@material_router.patch("/{id_material}",
                       response_model=Union[Material_Main, New_Response], tags=[Tags.material])
def edit_material(item: Annotated[Material_Main, Body(embed=True, description="Изменение данных материала по id")],
                  id_material: int, db: Session = Depends(get_session)):
    material = db.query(Material).filter(Material.id_material == id_material).first()
    if material is None:
        return JSONResponse(status_code=404, content={"message": "Материал не найден"})

    if item.name_material is not None:
        material.name_material = item.name_material
    if item.price is not None:
        material.price = item.price
    if item.id_type is not None:
        material.id_type = item.id_type
    if item.id_smell is not None:
        material.id_smell = item.id_smell
    if item.id_manufacturer is not None:
        material.id_manufacturer = item.id_manufacturer

    try:
        db.commit()
        db.refresh(material)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"message": f"Произошла ошибка при обновлении объекта: {str(e)}"})
    return material
