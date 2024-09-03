from pydantic import BaseModel


class BaseRecipe(BaseModel):
    dish_name: str
    views: int
    cooking_time: int


class RecipeIn(BaseRecipe):
    ingredients: str
    description: str


class RecipeOut(RecipeIn):
    id: int

    class Config:
        orm_mode = True


class RecipeShortenedOut(BaseRecipe):
    ...

    class Config:
        orm_mode = True
        
