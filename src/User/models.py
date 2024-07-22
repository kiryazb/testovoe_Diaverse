from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    second_name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    avatar: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
