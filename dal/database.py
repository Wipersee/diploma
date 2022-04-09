import databases
from sqlalchemy import create_engine, MetaData

SQLALCHEMY_DATABASE_URL = "postgres+psycopg2://myusername:mypassword@localhost/app"

database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()
