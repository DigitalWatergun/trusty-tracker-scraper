from sqlalchemy import Column, String, Numeric
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TrackingHist(Base):
    __tablename__ = "tracking_hist"
    id = Column(Numeric, primary_key=True)
    tracking_id = Column(String)
    utc_date = Column(String)
    status = Column(String)
    location = Column(String)
