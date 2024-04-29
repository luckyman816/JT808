from server import start_server
from sqlalchemy import create_engine
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .db.Vehicle import Base

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 8080
    engine = create_engine('D:\\Project\\JT808\\vehicle_data.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    start_server(HOST, PORT)