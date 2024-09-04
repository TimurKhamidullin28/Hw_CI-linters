from sqlalchemy import Column, Integer, String 

from database import Base


class Recipe(Base):
    __tablename__ = "Recipe"
    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, index=True)
    views = Column(Integer, index=True)
    time = Column(Integer, index=True)
    ingredients = Column(String, index=True)
    description = Column(String, index=True)
