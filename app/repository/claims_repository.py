from typing import List
from app.database import database_connection
from app.database.models import ClaimModel

class ClaimsRepository:
    def __init__(self):
        self.db = database_connection.session
  
    def create(self, new_claim_dict: dict) -> dict:
        new_claim = ClaimModel(**new_claim_dict)
        self.db.add(new_claim)
        self.db.commit()
        self.db.refresh(new_claim)
        return self.__to_dict(new_claim)
    
    def get_list(self, limit: int, offset: int) -> List[dict]:
        claims = self.db.query(ClaimModel).order_by("id").limit(limit).offset(offset).all()
        return [self.__to_dict(claim) for claim in claims]
    
    def get_by_id(self, claim_id: int) -> dict | None:
        claim = self.__get_one(claim_id)
        if claim is None:
            return None
        return self.__to_dict(claim)
    
    def update(self, claim_id: int, new_data: dict) -> dict | None:
        claim = self.__get_one(claim_id)
        if claim is None:
            return None
        for key, value in new_data.items():
            setattr(claim, key, value)
        self.db.commit()
        self.db.refresh(claim)
        return self.__to_dict(claim)
    
    def delete(self, claim_id: int) -> bool:
        claim = self.__get_one(claim_id)
        if claim is None:
            return False
        self.db.delete(claim)
        self.db.commit()
        return True
    
    
    def __get_one(self, claim_id: int) -> ClaimModel | None:
        return self.db.query(ClaimModel).filter(ClaimModel.id == claim_id).first()
    
    def __to_dict(self, claim: ClaimModel) -> dict:
        return {column.name: getattr(claim, column.name) for column in ClaimModel.__table__.columns}