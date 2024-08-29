from pydantic import BaseModel


class CategoryAddDTO(BaseModel):
    user_id: int
    name: str
    is_default: bool


class CategoryDTO(CategoryAddDTO):
    id: int
