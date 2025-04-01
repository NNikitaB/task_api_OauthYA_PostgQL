from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Sequence,Type,Any
from pydantic import BaseModel
from sqlalchemy.sql.expression import Select
from sqlalchemy import select,and_
from sqlalchemy.orm import Session
#from sqlalchemy.orm.unitofwork import UOWTransaction


T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    def list(self, **filters) -> List[T]:
        raise NotImplementedError()

    @abstractmethod
    def add(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def update(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError()



class BaseSqlRepository(BaseRepository[T], ABC):

    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    def _construct_get_stmt(self, id: int) -> Any:
        stmt = select(self._model_cls).where(getattr(self._model_cls, "id") == id)
        return stmt

    def get_by_id(self, id: int) -> Optional[T]:
        stmt = self._construct_get_stmt(id)
        return self._session.execute(stmt).scalar_one_or_none()

    def _construct_list_stmt(self, **filters) -> Any:
        stmt = select(self._model_cls)
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model_cls, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c) == v)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses))
        return stmt

    def list(self, **filters) -> List[T]:
        stmt = self._construct_list_stmt(**filters)
        result = self._session.execute(stmt)
        return list(result.scalars().all())

    def add(self, record: T) -> T:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def update(self, record: T) -> T:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def delete(self, id: int) -> None:
        record = self.get_by_id(id)
        if record is not None:
            self._session.delete(record)
            self._session.flush()

