from sqlalchemy import select

from .alchemy import SQLAlchemyRepository
from ..database import User
from ..types import UserDetail

__all__ = ["user_repository"]


class UserRepository(SQLAlchemyRepository):
    model = User
    schema = UserDetail

    def get_by_email(self, email: str):
        with self.session() as session:
            obj = session.scalar(
                select(self.model)
                .filter_by(email=email)
            )
            if obj is not None:
                return self.schema.model_validate(obj=obj, from_attributes=True)

    def activate(self, pk):
        with self.session() as session:
            user = session.get(self.model, pk)
            if user is not None:
                user.is_active = True
                session.commit()


user_repository = UserRepository()
