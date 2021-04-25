import sqlalchemy
from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    "jobs_to_categories",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("jobs", sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.id")),
    sqlalchemy.Column("category", sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
)


class Category(SqlAlchemyBase):
    __tablename__ = "categories"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
