from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase,Mapped, relationship, mapped_column
from app.domain.entities.user import User

class LinkModel(DeclarativeBase):
   id: Mapped[int] = mapped_column(primary_key=True,unique=True, nullable=False),
   original_url: Mapped[str] = mapped_column(String(255)),
   short_code: Mapped[str] = mapped_column(String(12), unique=True),
   user_id: Mapped[int]= mapped_column(),
   click_count: Mapped[int] = mapped_column(),
   users : Mapped[list[User]] = relationship("User", back_populates="link"),

   def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class UserModel(DeclarativeBase):
    id : Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    login : Mapped[str] = mapped_column(String(255))
    email : Mapped[str] = mapped_column(String(255))
    hashed_password : Mapped[str] = mapped_column(String(255))
    created_at : Mapped[datetime] = mapped_column(String(255))

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"