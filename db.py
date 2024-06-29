from config import settings
from sqlalchemy import create_engine
from models.classes import Base
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

ur_s = settings.POSTGRES_DATABASE_URLS
print(ur_s)

engine_s = create_engine(ur_s, echo=True)


Base.metadata.create_all(bind=engine_s)


def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()