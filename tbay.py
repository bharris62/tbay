from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://BHarris:@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Bid(Base):
    __tablename__ = 'bids'

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)

    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item = relationship('Item', backref='bids')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='bids')


Base.metadata.create_all(engine)

if __name__ == '__main__':
    from tbay import session
    from sqlalchemy import desc

    beyonce = User(username='bknowles', password='123456')
    christina = User(username='caguillera', password='qweasd')
    britney = User(username='bspears', password='secret')

    microphone = Item(name="microphone",
                      description="Mika's gold microphone.")

    bids = [
         Bid(price=500.0, user=christina, item=microphone),
         Bid(price=1150.0, user=beyonce, item=microphone),
         Bid(price=200.0, user=christina, item=microphone),
         Bid(price=201.0, user=beyonce, item=microphone),
    ]

    session.add_all([beyonce, christina, britney, microphone] + bids)
    session.commit()

    highest_bid = (session.query(Bid)
                   .filter(Bid.item==microphone)
                   .order_by(desc(Bid.price))
                   .first())

    print(highest_bid.user.username)
    print(highest_bid.item.description)