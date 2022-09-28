from sqlalchemy import Column, String, Numeric
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TrackingInfo(Base):
    __tablename__ = "tracking_info"
    tracking_id = Column(Numeric, primary_key=True)
    product_desc = Column(String)
    status = Column(String)
    carrier = Column(String)
    eta = Column(String)
