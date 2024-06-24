import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from routers.material_router import material_router, get_materials
from routers.manufacturer_router import manufacturer_router
from routers.technology_router import technology_router
from routers.smell_router import smell_router
from routers.gost_router import gost_router
from routers.parameter_router import parameter_router
from routers.type_router import type_router


app = FastAPI()


app.include_router(material_router)
app.include_router(parameter_router)
app.include_router(manufacturer_router)
app.include_router(technology_router)
app.include_router(gost_router)
app.include_router(type_router)
app.include_router(smell_router)


@app.get("/")
def main():
    return FileResponse("main_page.html")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
