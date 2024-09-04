from typing import List, Any

from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select

import models
import schemas
from database import async_engine, session

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await async_engine.dispose()


@app.post("/recipes/", response_model=schemas.RecipeOut)
async def recipes(recipe: schemas.RecipeIn) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.dict())
    async with session as async_session:
        async_session.add(new_recipe)
        await async_session.commit()
    return new_recipe


@app.get("/recipes/", response_model=List[schemas.RecipeShortenedOut])
async def get_recipes() -> List[schemas.RecipeShortenedOut]:
    res: Any = await session.execute(
        select(
            models.Recipe.dish_name, models.Recipe.views, models.Recipe.time
        ).order_by(models.Recipe.views.desc(), models.Recipe.time)
    )
    return [schemas.RecipeShortenedOut.from_orm(row) for row in res.all()]


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe(recipe_id: int) -> schemas.RecipeOut | tuple[str, int]:
    res: Any = await session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = res.scalar()
    if recipe:
        recipe.views += 1
        await session.commit()
        return schemas.RecipeOut.from_orm(recipe)
    else:
        raise HTTPException(status_code=404, detail="Recipe not found")
