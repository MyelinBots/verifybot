from sqlalchemy import create_engine
from .models.email import Base
Engine = create_engine("sqlite:///main.db", echo=True)

Base.metadata.create_all(Engine)