from datetime import datetime


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    tg_id = Column(BigInteger, nullable=False)
    city = Column(String)
    reports = relationship('WeatherReport', backref='weather_reports', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.tg_id


class WeatherReport(Base):
    __tablename__ = 'weather_reports'
    id = Column(Integer, primary_key=True)
    owner  = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    temp = Column(Integer, nullable=False)
    feels_like = Column(Integer, nullable=False)
    wind_speed = Column(Integer, nullable=False)
    pressure_mm = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    
    def __repr__(self):
        return f"{self.date} {self.temp} {self.city}"






# engine = create_engine('postgresql://postgres:SupBezSmetany0@localhost:5432/postgres', echo=True)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# book1 = session.query(Book).filter_by(title='Робинзон Крузо').first()
# film1 = Film(name='Невероятные приключения Робинзона', producer='Квентин Тарантино', book_id=book1.id)
# film2 = Film(name='Не правильный фильм', producer='Не Квентин Тарантино', book_id=book1.id)
# session.add(film1)
# session.add(film2)
# session.commit()