from typing import Annotated, Union
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Double
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum

Base = declarative_base()


class Gost(Base):
    __tablename__ = "gost"
    id_gost = Column(Integer, primary_key=True, autoincrement=True)
    name_gost = Column(String, index=True, nullable=False)

    materials = relationship("Material")


class Gost_Main(BaseModel):
    id_gost: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name_gost: Union[str, None] = 'unknown'


class Manufacturer(Base):
    __tablename__ = "manufacturer"
    id_manufacturer = Column(Integer, primary_key=True, autoincrement=True)
    name_manufacturer = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)


class Manufacturer_Main(BaseModel):
    id_manufacturer: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name_manufacturer: Union[str, None] = 'unknown'
    country: Union[str, None] = 'unknown'


class Parameter(Base):
    __tablename__ = "parameter"
    id_parameter = Column(Integer, primary_key=True, autoincrement=True)
    name_parameter = Column(String, index=True, nullable=False)
    units = Column(String, index=True, nullable=False)

    material_parameters = relationship("Material_parameters", back_populates="parameter")


class Parameter_Main(BaseModel):
    name_parameter: Union[str, None] = 'unknown'
    units: Union[str, None] = 'unknown'
    value_parameter: Union[float, None] = 0.0


class Material_parameters(Base):
    __tablename__ = "material_parameters"
    id_material = Column(Integer, ForeignKey('material.id_material'), primary_key=True)
    id_parameter = Column(Integer, ForeignKey('parameter.id_parameter'), primary_key=True)
    value_parameter = Column(Double, index=True, nullable=False)

    material = relationship("Material", back_populates="material_parameters")
    parameter = relationship("Parameter", back_populates="material_parameters")


class Smell(Base):
    __tablename__ = "smell"
    id_smell = Column(Integer, primary_key=True, autoincrement=True)
    degree_smell = Column(String, index=True, nullable=False)


class Smell_Main(BaseModel):
    id_smell: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    degree_smell: Union[str, None] = 'unknown'


class Type_of_material(Base):
    __tablename__ = "type_of_material"
    id_type = Column(Integer, primary_key=True, autoincrement=True)
    name_type = Column(String, index=True, nullable=False)


class Type_of_material_Main(BaseModel):
    name_type: Union[str, None] = 'unknown'


class Printing_technology(Base):
    __tablename__ = "printing_technology"
    id_technology = Column(Integer, primary_key=True, autoincrement=True)
    name_technology = Column(String, index=True, nullable=False)

    materials = relationship("Material")


class Printing_technology_Main(BaseModel):
    name_technology: Union[str, None] = 'unknown'


class Material(Base):
    __tablename__ = "material"
    id_material = Column(Integer, primary_key=True, autoincrement=True)
    name_material = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    id_manufacturer = Column(Integer, ForeignKey('manufacturer.id_manufacturer'))
    id_smell = Column(Integer, ForeignKey('smell.id_smell'))
    id_type = Column(Integer, ForeignKey('type_of_material.id_type'))
    id_gost = Column(Integer, ForeignKey('gost.id_gost'))
    id_technology = Column(Integer, ForeignKey('printing_technology.id_technology'))

    material_parameters = relationship("Material_parameters", back_populates="material")


class Material_Main(BaseModel):
    id_material: int | None = None
    name_material: str | None = 'material'
    price: float | None = 0.0
    technology: str | None = 'material'
    name_gost: str | None = 'unknown'
    degree_smell: str | None = 'unknown'
    name_manufacturer: str | None = 'unknown'
    country: str | None = 'unknown'


class Material_with_parameters_Main(BaseModel):
    id_material: int | None = None
    name_material: str | None = 'material'
    price: float | None = 0.0
    name_gost: str | None = 'unknown'
    degree_smell: str | None = 'unknown'
    name_manufacturer: str | None = 'unknown'
    country: str | None = 'unknown'
    parameters: list[Parameter_Main] | None = []


class Tags(Enum):
    material = "material"
    technology = "technology"
    gost = "gost"
    parameter = "parameter"
    smell = "smell"
    manufacturer = "manufacturer"
    type = "type"


class New_Response(BaseModel):
    message: str
