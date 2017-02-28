from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

username = 'root'
password = 'root'
host = 'localhost'
port = '3306'
schema = 'douban'
engine = create_engine("mysql+mysqlconnector://%s:%s@%s:%s/%s" % (username, password, host, port, schema))
DBSession = sessionmaker(bind=engine, expire_on_commit=False)

