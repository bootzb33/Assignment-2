from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, validator
import uvicorn

app = FastAPI()

class Rectangle(BaseModel):
    width: float = Field(gt=0, description="Width of the rectangle")
    height: float = Field(gt=0, description="Height of the rectangle")

    @validator("width", "height")
    def validate_positive(cls, value):
        if value <= 0:
            raise ValueError("Width and height must be positive!")
        return value

    def area(self):
        return self.width * self.height

    def circumference(self):
        return 2 * (self.width + self.height)

@app.post("/rect/", status_code=status.HTTP_201_CREATED)
async def create_rect(rect: Rectangle):
    return {
        "width": rect.width,
        "height": rect.height,
        "area": rect.area(),
        "circumference": rect.circumference(),
    }

@app.get("/rect/properties/")
async def get_rectangle_properties(
    width: float = Query(gt=0, description="Width of the rectangle"),
    height: float = Query(gt=0, description="Height of the rectangle")
):
    rect = Rectangle(width=width, height=height)
    return {
        "width": rect.width,
        "height": rect.height,
        "area": rect.area(),
        "circumference": rect.circumference(),
    }

if __name__ == "__main__":
    uvicorn.run("thursday:app", reload=True, workers=1)
