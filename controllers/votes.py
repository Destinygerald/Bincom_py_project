from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.votes_model import PuVote, Lga, LgaResult

class UserController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def allPollingResult (self):
        result = await self.db.execute(select(PuVote))
        return {'status': 'success', 'data': result.scalars().all()}

    async def sumTotal (self, lga_id: int):
        lga_find = await self.db.execute(select(Lga).where(Lga.lga_id == lga_id))
        lga_exists = lga_find.scalars().first()

        if not lga_exists:
            return { 'status': 'failed', 'error': 'Invalid LGA ID' }
        
        result_find = await self.db.execute(select(LgaResult).where(LgaResult.lga_name == lga_id))
        result = result_find.scalars().all()


        processed_data = []
        for item in result:
            
            # has_party = next(any(res.get('party') == item.party_abbreviation for res in processed_data), None)
            if len(processed_data) == 0:
                data = {
                    'lga_name': item.lga_name,
                    'total': item.party_score,
                    'party': item.party_abbreviation
                }
                processed_data.append(data)

            else:

                has_party = any(res for res in processed_data if res.get('party') == item.party_abbreviation)
                # prsint(f"************** {has_party}")
                # return
                if has_party:
                    for data in processed_data:    
                        if item.party_abbreviation == data['party']:
                            data['total'] += item.party_score
                        
                else:
                        data = {
                            'lga_name': item.lga_name,
                            'total': item.party_score,
                            'party': item.party_abbreviation
                        }
                        processed_data.append(data)

        return {'status': 'success', 'data': processed_data}
        

    async def storePollingRes (self, polling_unit_uniqueid: int, party_abbreviation: str, party_score: int, entered_by_user: str, date_entered: str, user_ip_address: str):
        lga_find = await self.db.execute(select(PuVote).where(PuVote.party_abbreviation == party_abbreviation and PuVote.polling_unit_uniqueid == polling_unit_uniqueid))
        lga_exists = lga_find.scalars().first()


        if lga_exists:
            return { 'status': 'failed', 'error': f'Result exists for this Party{party_abbreviation} at the Polling unit' }
        
        new_res = PuVote(polling_unit_uniqueid=polling_unit_uniqueid, 
                         party_abbreviation=party_abbreviation, 
                         party_score=party_score, 
                         entered_by_user=entered_by_user, 
                         date_entered=date_entered, 
                         user_ip_address=user_ip_address);
        self.db.add(new_res)
        await self.db.commit()
        await self.db.refresh(new_res)

        return {'status': 'success', 'data': new_res}
