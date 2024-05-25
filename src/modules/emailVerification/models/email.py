from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Email(Base):
    __tablename__ = "email_verification"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(60))
    name: Mapped[Optional[str]]
    nick: Mapped[str] = mapped_column(String(60))
    last_sent: Mapped[Optional[int]]
    
    def __repr__(self) -> str:
        return f"Email(id={self.id!r}, email={self.email!r}, name={self.name!r}), nick={self.nick!r}"

class Code(Base):
    __tablename__ = "code"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_id: Mapped[int] = mapped_column(ForeignKey("email_verification.id"))
    secret: Mapped[str] = mapped_column(String(60))
    def __repr__(self) -> str:
        return f"Code(id={self.id!r}, email_id={self.email_id!r})"