from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import Column, String, Integer

dev_env = True

if dev_env:

	DB_HOST = 'localhost'
	DB_USER = 'root'
	DB_PASSWORD = '###'

else:

	DB_HOST = '192.168.2.103'
	DB_USER = '##'
	DB_PASSWORD = '###'

DB_BASE_URI = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':3306'
DB_URI = DB_BASE_URI + '/HomeWebServer?charset=utf8'
engine = create_engine(DB_URI, isolation_level="READ COMMITTED", poolclass=NullPool)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()
Base = declarative_base()


class Configuration(Base):
	__tablename__ = "Configuration"

	id = Column("Id", Integer, primary_key=True)
	name = Column("Name", String(50))
	value = Column("Value", String(50))
	description = Column("Description", String(50))
