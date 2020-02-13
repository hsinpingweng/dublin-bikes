import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Forecast(Base):
    __tablename__ = 'forecasts'
    timestamp = Column(String(30), primary_key=True)
    temperature = Column(String(10))
    description = Column(String(30))
    icon = Column(String(30))


def scrape():
    host = 'database-1.cmv75f0i1uzy.eu-west-1.rds.amazonaws.com'
    engine = create_engine(f"mysql://dev:qwerty@{host}/development")
    Base.metadata.create_all(engine)  # Create table
    Session = sessionmaker(bind=engine)
    session = Session()

    key = '9045a4958d8f45e1a54f6607ff2ed1d2'
    city = 'Dublin'
    country = 'IE'
    hours = 6
    api = f'https://api.weatherbit.io/v2.0/forecast/hourly?city={city}&country={country}&hours={hours}&key={key}'

    response = requests.get(api)
    if response:
        session.execute('TRUNCATE TABLE forecasts')  # clear the table
        response = response.json()
        for forecast in response['data']:
            timestamp = forecast['timestamp_local']
            temperature = forecast['temp']
            description = forecast['weather']['description']
            icon = forecast['weather']['icon']
            session.add(Forecast(timestamp=timestamp, temperature=temperature,
                                 description=description, icon=icon))
        session.commit()
    else:
        print('Error')


scrape()
