import os
import sys
from sqlalchemy import Column, Integer, String, DateTime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from _config.db import Base




class PuVote(Base):
    __tablename__ = "announced_pu_results"
    
    result_id = Column(Integer, primary_key=True)
    polling_unit_uniqueid = Column(String(50))
    party_abbreviation = Column(String(4))
    party_score = Column(Integer)
    entered_by_user = Column(String(50))
    date_entered = Column(DateTime)
    user_ip_address = Column(String(50))
    # __table__ = Table('announced_pu_results', Base.metadata, autoload_with=sync_engine)


class Lga(Base):
    __tablename__ = "lga"
    
    uniqueid = Column(Integer, primary_key=True) 
    lga_id = Column(Integer) 
    lga_name = Column(String(50)) 
    state_id = Column(Integer) 
    lga_description = Column(String) 
    entered_by_user = Column(String(50)) 
    date_entered = Column(DateTime) 
    user_ip_address = Column(String(50))




class LgaResult(Base):
    __tablename__ = "announced_lga_results"

    result_id = Column(Integer, primary_key=True) 
    lga_name = Column(String(50)) 
    party_abbreviation = Column(String(4)) 
    party_score = Column(Integer) 
    entered_by_user = Column(String(50)) 
    date_entered = Column(DateTime) 
    user_ip_address = Column(String(50))