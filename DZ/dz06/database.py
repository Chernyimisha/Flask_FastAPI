import databases
import sqlalchemy
from sqlalchemy.orm import session


DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128))
)

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(1000)),
    sqlalchemy.Column("price", sqlalchemy.Float)
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("date", sqlalchemy.DateTime()),
    sqlalchemy.Column("status", sqlalchemy.String(15), nullable=False),
    sqlalchemy.Column("id_user", sqlalchemy.Integer, sqlalchemy.ForeignKey(users.c.id)),
    sqlalchemy.Column("id_goods", sqlalchemy.Integer, sqlalchemy.ForeignKey(goods.c.id))
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


def count_rows(table_class):
    with engine.connect() as connect:
        result = connect.scalar(sqlalchemy.select(sqlalchemy.func.max(table_class.c.id)))
        return result

