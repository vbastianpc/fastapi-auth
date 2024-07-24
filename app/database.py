from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase  # , MappedAsDataclass
from sqlalchemy.orm import sessionmaker

path_db = Path(__file__).parent.relative_to(Path.cwd()) / "sql_app.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{path_db}"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#integration-with-annotated
# class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
#     pass


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
