from typing import Annotated, Union, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Double, Table
from sqlalchemy.orm import declarative_base, relationship, Mapped
from enum import Enum

Base = declarative_base()


class Gost_material(Base):
    __tablename__ = "gost_material"
    id_material = Column(Integer, ForeignKey('material.id_material'), primary_key=True)
    id_gost = Column(Integer, ForeignKey('gost.id_gost'), primary_key=True)

    material = relationship("Material", back_populates="gost_materials")
    gost = relationship("Gost", back_populates="gost_materials")

class Gost(Base):
    __tablename__ = "gost"
    id_gost = Column(Integer, primary_key=True, autoincrement=True)
    name_gost = Column(String, index=True, nullable=False)

    # materials = relationship("Gost_material", backref='gost')
    gost_materials = relationship("Gost_material", back_populates="gost")


class Gost_Main(BaseModel):
    id_gost: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name_gost: Union[str, None] = None


class Manufacturer(Base):
    __tablename__ = "manufacturer"
    id_manufacturer = Column(Integer, primary_key=True, autoincrement=True)
    name_manufacturer = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)



class Manufacturer_Main(BaseModel):
    id_manufacturer: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name_manufacturer: Union[str, None] = None
    country: Union[str, None] = None


class Parameter(Base):
    __tablename__ = "parameter"
    id_parameter = Column(Integer, primary_key=True, autoincrement=True)
    name_parameter = Column(String, index=True, nullable=False)

    material_parameters = relationship("Material_parameters", back_populates="parameter")


class Parameter_Main(BaseModel):
    id_parameter: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name_parameter: Union[str, None] = None


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
    degree_smell: Union[str, None] = None


class Type_of_material(Base):
    __tablename__ = "type_of_material"
    id_type = Column(Integer, primary_key=True, autoincrement=True)
    name_type = Column(String, index=True, nullable=False)


class Type_of_material_Main(BaseModel):
    name_type: Union[str, None] = None


class Printing_technology(Base):
    __tablename__ = "printing_technology"
    id_technology = Column(Integer, primary_key=True, autoincrement=True)
    name_technology = Column(String, index=True, nullable=False)


class Printing_technology_Main(BaseModel):
    name_technology: Union[str, None] = None


class Material(Base):
    __tablename__ = "material"
    id_material = Column(Integer, primary_key=True, autoincrement=True)
    name_material = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    id_manufacturer = Column(Integer, ForeignKey('manufacturer.id_manufacturer'))
    id_smell = Column(Integer, ForeignKey('smell.id_smell'))
    id_type = Column(Integer, ForeignKey('type_of_material.id_type'))

    # gosts = relationship("Gost_material", backref='material')
    gost_materials = relationship("Gost_material", back_populates="material")
    material_parameters = relationship("Material_parameters", back_populates="material")


class Material_Main(BaseModel):
    name_material: Union[str, None] = None
    price: Union[float, None] = None
    name_gost: Union[str, None] = None
    degree_smell: Union[str, None] = None


class Technology_material(Base):
    __tablename__ = "technology_material"
    id_material = Column(Integer, ForeignKey('material.id_material'), primary_key=True)
    id_technology = Column(Integer, ForeignKey('printing_technology.id_technology'), primary_key=True)


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
