from pydantic import BaseModel

class ResultCreate(BaseModel):
    polling_unit_uniqueid : int
    party_abbreviation : str
    party_score : int
    entered_by_user : str
    date_entered : str
    user_ip_address : str