from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

from sqlalchemy import Select
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger import AppLogger
from src.exceptions import SqlAlchemyError
from src.schemas.dtos import BaseSchema
from src.models import MixinAutoIdModel


ModelType = TypeVar('ModelType', bound=MixinAutoIdModel)
ShortDto = TypeVar('ShortDto', bound=BaseSchema)
FullDto = TypeVar('FullDto', bound=BaseSchema)


class BaseRepositoryInterface:
    """
    Базовый интерфейс репозитория.
    """
    pass


class BaseDbRepository(BaseRepositoryInterface, Generic[ModelType, ShortDto, FullDto]):
    """
    Базовый репозиторий для работы с БД.
    """

    def __init__(
            self,
            async_db_session: AsyncSession,
            model_type: Type[ModelType],
            short_dto_type: Type[ShortDto],
            full_dto_type: Type[FullDto],
            schemas_to_models_dict: Optional[
                Dict[Type[BaseSchema], Type[MixinAutoIdModel]]
            ] = None,
            short_select_statement: Optional[Select[Tuple[ModelType]]] = None,
            full_select_statement: Optional[Select[Tuple[ModelType]]] = None
    ):
        self._async_db_session = async_db_session
        self._model_type = model_type
        self._short_dto_type = short_dto_type
        self._full_dto_type = full_dto_type

        default_schemas_to_models_dict: Dict[Type[BaseSchema], Type[MixinAutoIdModel]] = {
            short_dto_type: model_type,  # type: ignore[dict-item]
            full_dto_type: model_type,  # type: ignore[dict-item]
        }
        if schemas_to_models_dict:
            schemas_to_models_dict.update(default_schemas_to_models_dict)
        else:
            schemas_to_models_dict = default_schemas_to_models_dict
        self._schemas_correspond_models_dict = schemas_to_models_dict

        if short_select_statement is None:
            short_select_statement = select(model_type)
        self._short_select_statement = short_select_statement

        if full_select_statement is None:
            full_select_statement = select(model_type)
        self._full_select_statement = full_select_statement

    @property
    def async_db_session(self) -> AsyncSession:
        """
        Получение асинхронной сессии БД.

        :return: Асинхронная сессия.
        """
        return self._async_db_session

    @property
    def model_type(self) -> Type[ModelType]:
        """
        Получение класса основной модели ORM.

        :return: Класс модели ORM.
        """
        return self._model_type

    @property
    def short_schema_type(self) -> Type[ShortDto]:
        """
        Получение краткого DTO.

        :return: Краткое DTO.
        """
        return self._short_dto_type

    @property
    def full_schema_type(self) -> Type[FullDto]:
        """
        Получение полного DTO.

        :return: Полное DTO.
        """
        return self._full_dto_type

    @property
    def schemas_correspond_models_dict(self) -> Dict[Type[BaseSchema], Type[MixinAutoIdModel]]:
        """
        Получение словаря соответствия схем DTO и модели ORM.

        :return: Словарь соответствия схем DTO и модели ORM.
        """
        return self._schemas_correspond_models_dict

    @property
    def short_select_statement(
            self
    ) -> Select[Tuple[ModelType]]:
        """
        Получение краткой формы SELECT.

        :return: Краткая форма SELECT.
        """
        return self._short_select_statement

    @property
    def full_select_statement(
            self
    ) -> Select[Tuple[ModelType]]:
        """
        Получение полной формы SELECT.

        :return: Полная форма SELECT.
        """
        return self._full_select_statement

    async def commit(self) -> None:
        """
        Фиксация изменений в БД.

        :return: None.
        """
        AppLogger.debug('Commit some changes in DB')
        try:
            await self._async_db_session.commit()
        except Exception as e:
            await self._async_db_session.rollback()
            AppLogger.error(f"Ошибка при коммите: {e}")
        finally:
            await self._async_db_session.close()

    async def merge(self, model: ModelType) -> ModelType:
        """
        Слияние модели с данными в БД.

        :param model: Модель ORM.
        :return: None.
        """
        AppLogger.debug(f'Merge model: {model}')

        model = await self._async_db_session.merge(model)
        await self._async_db_session.flush()

        return model

    def convert_schema_to_orm_model(self, schema: BaseSchema) -> ModelType:
        """
        Преобразование схемы в модель.

        :param schema: Схема Pydantic.
        :return: ORM модель SQLAlchemy.
        """
        AppLogger.debug(f'Convert schema to orm model: {schema}')

        model_dict: Dict[str, Any] = dict()
        for key, value in schema:
            if issubclass(type(value), BaseSchema):
                model_dict[key] = self.convert_schema_to_orm_model(value)
            elif isinstance(value, list):
                new_list = list()
                for item in value:
                    if issubclass(item.__class__, BaseSchema):
                        new_list.append(self.convert_schema_to_orm_model(item))
                    else:
                        new_list.append(item)
                model_dict[key] = new_list
            elif key == 'id' and not value:
                continue
            else:
                model_dict[key] = value
        model_class = self._schemas_correspond_models_dict[type(schema)]

        return model_class(**model_dict)  # type: ignore[return-value]

    async def execute_select_one_statement(
            self,
            select_statement: Select  # type: ignore[type-arg]
    ) -> Optional[MixinAutoIdModel]:
        """
        Выполнение SELECT запроса для выборки одного объекта из БД.

        :param select_statement: Выражение SELECT.
        :return: Объект ORM.
        """
        AppLogger.debug(f'Execute select statement: {select_statement}')

        return await self._async_db_session.scalar(  # type: ignore[no-any-return]
            select_statement
        )

    async def execute_select_many_statement(
            self,
            select_statement: Select  # type: ignore[type-arg]
    ) -> List[MixinAutoIdModel]:
        """
        Выполнение SELECT запроса для выборки множества объектов из БД.

        :param select_statement: Выражение SELECT.
        :return: Список объектов ORM.
        """
        AppLogger.debug(f'Execute select statement: {select_statement}')

        result = await self._async_db_session.execute(select_statement)

        return list(result.scalars().unique().all())

    async def upsert(self, dto: FullDto) -> FullDto:
        """
        Обновление или создание объекта в БД.

        :param dto: Данные для обновления или создания объекта.
        :return: Обновленный или созданный объект.
        """
        AppLogger.debug(f'Upsert object: {dto.model_dump()}')

        model = self.convert_schema_to_orm_model(schema=dto)
        try:
            model = await self.merge(model=model)

            return self._full_dto_type.model_validate(obj=model)
        except IntegrityError as exc:
            AppLogger.error(f'IntegrityError {exc}. Data: {dto.model_dump()}')

            raise SqlAlchemyError()

    async def upsert_many(self, dto_list: List[FullDto]) -> List[FullDto]:
        """
        Обновление или создание списка объектов в БД.

        :param dto_list: Список данных для обновления или создания объектов.
        :return: Список обновленных или созданных объектов.
        """
        AppLogger.debug(f'Upsert many objects: {dto_list}')

        models = [self.convert_schema_to_orm_model(schema=dto) for dto in dto_list]
        try:
            for i in range(len(models)):
                models[i] = await self.merge(model=models[i])
            await self.commit()
            return [self._full_dto_type.model_validate(obj=model) for model in models]
        except IntegrityError as exc:
            AppLogger.error(f'IntegrityError {exc}. Data: {dto_list}')

            raise SqlAlchemyError()

    async def get_one_full_by_id(self, object_id: int) -> Optional[FullDto]:
        """
        Выборка одного полного DTO объекта из БД через метод сессии.

        :param object_id: ID объекта.
        :return: Полное DTO объекта или None.
        """
        AppLogger.debug(f'Select one object full DTO: {object_id}')

        model = await self._async_db_session.get(self._model_type, object_id)
        if model:
            return self._full_dto_type.model_validate(obj=model)

        return None

    async def select_one_full_by_id(self, object_id: int) -> Optional[FullDto]:
        """
        Выборка одного полного DTO объекта из БД через SELECT.

        :param object_id: ID объекта.
        :return: Полное DTO объекта или None.
        """
        AppLogger.debug(f'Select one object full DTO: {object_id}')

        model = await self.execute_select_one_statement(
            select_statement=self._full_select_statement.where(self._model_type.id == object_id)
        )
        if model:
            return self._full_dto_type.model_validate(obj=model)

        return None

    async def select_all_full(self) -> List[FullDto]:
        """
        Выборка всех полных DTO объектов из БД.

        :return: Список полных DTO объектов.
        """
        AppLogger.debug(f'Select all objects {self._model_type}')

        models_list = await self.execute_select_many_statement(select_statement=self._full_select_statement)

        return [self._full_dto_type.model_validate(obj=model) for model in models_list]

    async def select_all_short(self) -> List[ShortDto]:
        """
        Выборка всех кратких DTO объектов из БД.

        :return: Список кратких DTO объектов.
        """
        AppLogger.debug(f'Select all objects {self._model_type}')

        models_list = await self.execute_select_many_statement(select_statement=self._short_select_statement)

        return [self._short_dto_type.model_validate(obj=model) for model in models_list]

    async def delete(self, object_id: int) -> bool:
        """
        Удаление объекта из БД по идентификатору.

        :param object_id: ID объекта.
        :return: Статус удаления.
        """
        AppLogger.debug(f'Delete object: {object_id}')

        statement = delete(
            self._model_type
        ).where(
            self._model_type.id == object_id
        )
        result = await self._async_db_session.execute(statement)
        await self.commit()
        return result.rowcount == 1

    async def delete_many(self, objects_ids_list: List[int]) -> bool:
        """
        Удаление нескольких объектов из БД по идентификатору.

        :param objects_ids_list: Список ID объектов.
        :return: Статус удаления.
        """
        AppLogger.debug(f'Delete objects: {objects_ids_list}')

        statement = delete(
            self._model_type
        ).where(
            self._model_type.id.in_(
                objects_ids_list
            )
        )
        result = await self._async_db_session.execute(statement)
        await self.commit()
        return result.rowcount == len(objects_ids_list)
