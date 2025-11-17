from sqlalchemy.orm import DeclarativeBase

class LinkModel(DeclarativeBase):
   id: Mapped[int] = mapped_column(primary_key=True,unique=True, nullable=False),
   original_url: Mapped[str] = mapped_column(String(255)),
   short_code: Mapped[str] = mapped_column(String(12), unique=True),
   user_id: Mapped[int]= mapped_column(),
   click_count: Mapped[int] = mapped_column()

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class UserModel(DeclarativeBase):
    id : Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    login : Mapped[str] = mapped_column(String(40))
    email : Mapped[str] = mapped_column(String())
    hashed_password : Mapped[str]
    created_at : datetime