from main_service.src.infrastructure.repositories.db_repo import database_repository
from main_service.src.infrastructure.models.category import CategoriesOrm
from main_service.src.domain.entities.category import CategoryAddDTO, CategoryDTO
from main_service.src.infrastructure.repositories.base_crud_repo import BaseRepository
from sqlalchemy import select, or_


class CategoryRepository(BaseRepository[CategoryDTO, CategoryAddDTO]):
    repository = database_repository

    @classmethod
    def orm_model(cls) -> type:
        return CategoriesOrm

    @classmethod
    def add_dto_model(cls) -> type:
        return CategoryAddDTO

    @classmethod
    def dto_model(cls) -> type:
        return CategoryDTO

    @classmethod
    async def find_all_by_user_id(
        cls, user_id: int, limit: int, offset: int
    ) -> list[CategoryDTO]:
        async with cls.repository.a_sessionmaker() as new_session:
            query = (
                select(CategoriesOrm)
                .where(
                    or_(
                        CategoriesOrm.user_id == user_id,
                        CategoriesOrm.is_default == True,
                    )
                )
                .limit(limit)
                .offset(offset)
                .order_by(CategoriesOrm.id)
            )
            result = await new_session.execute(query)
            orm_list = result.unique().scalars().all()
            dto_list = [
                CategoryDTO.model_validate(row, from_attributes=True)
                for row in orm_list
            ]
            return dto_list
