from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql://root:1234567@localhost:3306/enrollment_db'

engine = create_engine(DATABASE_URL)
Base = declarative_base()
class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    status = Column(Enum('Pending', 'Enrolled', 'Rejected'), default='Pending')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
